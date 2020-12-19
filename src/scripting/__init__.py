import obspython as obs
from helpers.obs_context_manager import source_list_ar


def fill_source_list(p):
    obs.obs_property_list_clear(p)
    obs.obs_property_list_add_string(p, "", "")
    with source_list_ar() as sources:
        if sources is not None:
            for source in sources:
                source_id = obs.obs_source_get_unversioned_id(source)
                if (
                    source_id == "text_gdiplus" or
                    source_id == "text_ft2_source"
                ):
                    name = obs.obs_source_get_name(source)
                    obs.obs_property_list_add_string(p, name, name)
