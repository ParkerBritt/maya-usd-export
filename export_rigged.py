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

def export(output=None, debug=False):
    export_usd.ExportAnim(
        geo_whitelist=["render", "skeleton"],
        usd_type="xform",
        output=output,
        debug=debug,
    )
