from contextlib import contextmanager

import obspython as obs

# auto release context managers


@contextmanager
def source_ar(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


@contextmanager
def p_source_ar(id, source_name, settings):
    try:
        _source = obs.obs_source_create_private(id, source_name, settings)
        yield _source
    finally:
        obs.obs_source_release(_source)


@contextmanager
def data_ar(source_settings=None):
    settings = None
    if not source_settings:
        settings = obs.obs_data_create()
    if source_settings:
        settings = obs.obs_source_get_settings(source_settings)
    try:
        yield settings
    finally:
        obs.obs_data_release(settings)


@contextmanager
def scene_ar(scene):
    scene = obs.obs_scene_from_source(scene)
    try:
        yield scene
    finally:
        obs.obs_scene_release(scene)


@contextmanager
def filter_ar(source, name):
    source = obs.obs_source_get_filter_by_name(source, name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


@contextmanager
def source_list_ar():
    source_list = obs.obs_enum_sources()
    try:
        yield source_list
    finally:
        obs.source_list_release(source_list)


@contextmanager
def media_source_ar(media_path: str, monitoring_type: int):
    media_source = obs.obs_source_create_private(
        "ffmpeg_source", "Global Media Source", None
        )
    with data_ar() as settings:
        obs.obs_data_set_string(settings, "local_file", media_path)
        obs.obs_source_update(media_source, settings)
        obs.obs_source_set_monitoring_type(media_source, monitoring_type)
        try:
            yield media_source
        finally:
            obs.obs_source_release(media_source)
