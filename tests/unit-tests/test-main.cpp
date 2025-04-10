#include <catch2/catch_test_macros.hpp>
#include "export.h"

TEST_CASE( "Test export", "[export]" ) {
    REQUIRE( 1 == 1 );
    foo();
    // REQUIRE( 1 != 1 );
}
