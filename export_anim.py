import traceback, importlib
if __name__ == "__main__":
    from . import export_usd
else:
    try:
        import export_usd
    except:
        traceback.print_exc()
        exit()
importlib.reload(export_usd)


def export(output=None, debug=False, start_frame=None, end_frame=None, include_blendshapes=False):
    if not output:
        output = "/home/will/Downloads/test_usd_export/{character}.usd"
    export_usd.ExportAnim(
        geo_whitelist=["render"],
        usd_type="",
        output=output,
        debug=debug,
        export_rig=False,
        start_frame=start_frame,
        end_frame=end_frame,
        include_blendshapes=include_blendshapes
    )
