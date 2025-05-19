def pytest_addoption(parser):
    parser.addoption(
        "--keep-tmp-dirs",
        action="store_true",
        default=False,
        help="Don't destroy tmp dirs after tests",
    )

