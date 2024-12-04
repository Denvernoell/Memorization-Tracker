from .utils import STable, TableColumn, AGOTable
from pydantic import Field, TypeAdapter
from typing_extensions import Annotated

bigstr = TypeAdapter(Annotated[str, Field()])

contacts = STable(
    name="Contacts",
    supabase_table="AWD_contact_info",
    primary_key="index",
    columns=[
        TableColumn(field="full_name", name="Full Name", editable=False, type=str),
        TableColumn(field="email", name="Email", editable=True, type=str),
        TableColumn(
            field="primary_phone", name="Primary Phone", editable=True, type=str
        ),
        TableColumn(
            field="board_members_group", name="Board Member", editable=True, type=bool
        ),
        TableColumn(
            field="sgma_monitoring_group",
            name="SGMA Monitoring Group",
            editable=True,
            type=bool,
        ),
        TableColumn(
            field="interested_parties_group",
            name="Interested Party",
            editable=True,
            type=bool,
        ),
        TableColumn(
            field="notes",
            name="Notes",
            editable=True,
            type=str,
        ),
    ],
)

# table_a = STable(
#     name="Exhibit A",
#     supabase_table="AWD_zdrive_wells",
#     primary_key="DMS_Site_I",
#     columns=[
#         TableColumn(name="Well ID", field="DMS_Site_I", type=str, editable=False),
#         TableColumn(name="Well Diameter", field="Diameter", type=int, editable=True),
#     ],
# )

# T_well_info = STable(
#     name="Well Info",
#     supabase_table="AWD_zdrive_wells",
#     primary_key="DMS_Site_I",
#     columns=[
#         TableColumn(name="Well ID", field="DMS_Site_I", type=str, editable=False),
#         TableColumn(name="Well Diameter", field="Diameter", type=int, editable=True),
#         TableColumn(name="Well Depth", field="Total_Well", type=int, editable=True),
#     ],
# )

from enum import Enum


class Designation(Enum):
    Upper = "above corcoran"
    # Composite = "Composite"
    Lower = "below corcoran"
    # Unknown = "Unknown"
    # Nested = "Nested"


# class WCR(Enum):
#     Yes = "Yes"
#     No = "No"


class WellStatus(Enum):
    Active = "Active"
    Inactive = "Inactive"
    # Proposed = "Proposed"
    Destroyed = "Destroyed"


class WCR(Enum):
    Yes = "yes"
    No = "no"
    No_star = "no*"


class District(Enum):
    TID = "TID"
    FSWD = "FSWD"
    FC = "FC"


from pydantic_extra_types.coordinate import Longitude, Latitude, Coordinate
from datetime import date


T_municipal_pumping_gallons = STable(
    name="Municipal Pumping Gallons",
    supabase_table="TID_domestic_water_use_gallons",
    primary_key="index",
    columns=[
        TableColumn(name="Index", field="index", type=int, editable=False),
        TableColumn(name="Year", field="year", type=int, editable=True),
        TableColumn(name="Month", field="month", type=int, editable=True),
        TableColumn(
            name="Water Use Gallons",
            field="water_use_gallons",
            type=float,
            editable=True,
        ),
    ],
)

T_MonthlyExtractionAF = STable(
    name="Monthly Extraction AF",
    supabase_table="TID_full_extractions_monthly_AF",
    primary_key="index",
    columns=[
        TableColumn(name="Index", field="index", type=int, editable=False),
        TableColumn(name="Well ID", field="well_id", type=str, editable=True),
        TableColumn(name="Date", field="date", type=date, editable=True),
        TableColumn(
            name="Monthly Extraction AF",
            field="monthly_extraction_AF",
            type=float,
            editable=True,
        ),
    ],
)


T_surface_water_af = STable(
    name="Surface Water AF",
    supabase_table="TID_surface_water_melt",
    primary_key="index",
    columns=[
        TableColumn(name="Index", field="index", type=int, editable=False),
        TableColumn(name="Date", field="date", type=date, editable=True),
        TableColumn(name="Water Source", field="water_source", type=str, editable=True),
        TableColumn(name="Volume AF", field="volume_af", type=float, editable=True),
    ],
)


T_well_info = STable(
    name="Well Info",
    supabase_table="TID_well_locations",
    primary_key="well_id",
    # sort_columns=["DMS_Site_I"],
    columns=[
        TableColumn(name="Well ID", field="well_id", type=str, editable=False),
        TableColumn(name="Name", field="well_name", type=str, editable=True),
        # TableColumn(
        #     name="Alternative Name", field="Alternativ", type=str, editable=True
        # ),
        TableColumn(name="Status", field="well_status", type=WellStatus, editable=True),
        TableColumn(name="District", field="District", type=District, editable=True),
        TableColumn(
            name="Well Depth", field="total_well_depth", type=int, editable=True
        ),
        TableColumn(
            name="Perf Start 1",
            field="perforated_interval_top1",
            type=int,
            editable=True,
        ),
        TableColumn(
            name="Perf Stop 1",
            field="perforated_interval_bottom1",
            type=int,
            editable=True,
        ),
        TableColumn(
            name="Perf Start 2",
            field="perforated_interval_top2",
            type=int,
            editable=True,
        ),
        TableColumn(
            name="Perf Stop 2",
            field="perforated_interval_bottom2",
            type=int,
            editable=True,
        ),
        TableColumn(name="Clay Top", field="CorcClay_Top", type=int, editable=True),
        TableColumn(name="Clay Bottom", field="CorcClay_Bot", type=int, editable=True),
        # TableColumn(name="Well Diameter", field="Diameter", type=int, editable=True),
        TableColumn(name="Drill Date", field="date_drilled", type=date, editable=True),
        TableColumn(
            name="Aquifer Designation",
            field="aquifer_designation",
            type=Designation,
            editable=True,
        ),
        TableColumn(
            name="Notes",
            field="well_notes",
            type=str,
            editable=True,
        ),
        TableColumn(
            name="Path",
            field="path",
            type=str,
            editable=False,
        ),
    ],
)
