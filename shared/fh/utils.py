from fasthtml.common import *

from pathlib import Path

import sys

sys.path.append(str(Path(__file__).parent.parent))
from shared.database import supabase
# from shared.data.gis import ago

from typing import Union
import pydantic

from enum import Enum


class TableColumn(pydantic.BaseModel):
    name: str
    field: str
    type: type
    editable: bool


class STable(pydantic.BaseModel):
    name: str
    supabase_table: str
    primary_key: str
    columns: list[TableColumn]
    # rows: list[dict[str, str]]

    @property
    def table(self):
        return supabase.table(self.supabase_table)

    @property
    def select_cols(self):
        return ",".join([c.field for c in self.columns])

    @property
    def select(self):
        return self.table.select(self.select_cols)

    def fetch_rows(self):
        return (
            self.table.select(self.select_cols).order(self.primary_key).execute().data
        )

    def get_row_by_pk(self, pk_value):
        return (
            self.table.select(self.select_cols)
            .eq(self.primary_key, pk_value)
            .execute()
            .data[0]
        )

    def generate_display_row(self, row):
        return Tr(
            *[Td(get_display_item(row, c)) for c in self.columns],
            Td(
                Button(
                    cls="btn danger",
                    hx_get=f"/wells/{row[self.primary_key]}/edit",
                )("Edit")
            ),
        )

    def generate_edit_row(self, row):
        return Tr(
            hx_trigger="cancel",
            cls="editing",
            hx_get=f"/wells/{row[self.primary_key]}/row",
        )(
            *[Td(get_editable_table_cells(row, c)) for c in self.columns],
            Td(
                Button(
                    cls="btn danger",
                    hx_get=f"/wells/{row[self.primary_key]}/row",
                )("Cancel"),
                Button(
                    cls="btn danger",
                    hx_put=f"/wells/{row[self.primary_key]}",
                    hx_include="closest tr",
                )("Save"),
            ),
        )


class AGOTable(pydantic.BaseModel):
    # https://developers.arcgis.com/python/latest/api-reference/arcgis.features.toc.html#arcgis.features.FeatureLayer.query
    name: str
    ago_table_id: str
    layer_num: int
    primary_key: str
    columns: list[TableColumn]
    sort_columns: list[str]

    @property
    def layer(self):
        return ago.content.get(self.ago_table_id).layers[self.layer_num]

    # rows: list[dict[str, str]]
    def get_all(self, query="1=1", return_geometry=False):
        return (
            # ago.content.get(self.ago_table_id)
            # .layers[self.layer_num]
            self.layer.query(
                where=query,
                out_fields=",".join([c.field for c in self.columns]),
                return_geometry=return_geometry,
                order_by_fields=" ASC, ".join(self.sort_columns),
                # as_df=False,
            )
        )

    def get_list(self, query="1=1", return_geometry=False):
        return [r.attributes for r in self.get_all(query, return_geometry).features]

    def get_object_id(self, query):
        if len(self.get_list(query)) == 0:
            return ValueError("No object found.")
        if len(self.get_list(query)) > 1:
            raise ValueError("More than one object found.")
        else:
            return self.get_list(query)[0][self.primary_key]


def get_display_item(row, c):
    if c.type is bool:
        return Input(
            name=c.field,
            type="checkbox",
            checked=row[c.field],
            disabled=True,
        )

    elif c.type is str:
        return (P(row[c.field]),)

    elif c.type is int:
        return (P(row[c.field]),)

    elif c.type is float:
        return (P(row[c.field]),)

    elif c.type.__base__ is Enum:
        return (P(c.type(row[c.field]).value),)


def get_editable_item(row, c):
    print(row)
    if not c.editable:
        # return Td(
        #     P(row[c.field]),
        # )
        return get_display_item(row, c)
    else:
        if c.type is bool:
            return Input(
                name=c.field,
                type="checkbox",
                checked=row[c.field],
            )

        elif c.type is str:
            return Input(
                name=c.field,
                value=row[c.field],
                # hx_disable="true",
                cls="input input-bordered disabled",
            )

        elif c.type is int:
            return Input(
                name=c.field,
                value=row[c.field],
                type="number",
                cls="input input-bordered",
            )

        elif c.type is float:
            return Input(
                name=c.field,
                value=row[c.field],
                type="number",
                cls="input input-bordered",
            )

        elif c.type.__base__ is Enum:
            return Select(
                *mk_opts(
                    nm=c.name, cs=[e.value for e in c.type], selected=row[c.field]
                ),
                name=c.field,
                value=row[c.field],
            )


def get_editable_table_cells(row, c):
    return Td(get_editable_item(row, c))


def get_display_table_cells(row, c):
    return Td(get_display_item(row, c))


def mk_opts(nm, cs, selected=None):
    return (
        Option(
            f"-- select {nm} --",
            disabled="",
            # selected=selected is None,
            value="",
        ),
        *[
            Option(
                c,
                selected=c == selected,
                value=c,
            )
            for c in cs
        ],
    )
