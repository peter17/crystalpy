size_inclusions = 250;
size_holes = 300;
size_bulk = 250;

Point(1) = {-125, -125, 0, size_inclusions};
Point(2) = {-225, -125, 0, size_inclusions};
Point(3) = {-25, -125, 0, size_inclusions};
Point(4) = {-125, -125, 300, size_inclusions};
Point(5) = {-225, -125, 300, size_inclusions};
Point(6) = {-25, -125, 300, size_inclusions};
Point(7) = {-125, 125, 0, size_inclusions};
Point(8) = {-225, 125, 0, size_inclusions};
Point(9) = {-25, 125, 0, size_inclusions};
Point(10) = {-125, 125, 300, size_inclusions};
Point(11) = {-225, 125, 300, size_inclusions};
Point(12) = {-25, 125, 300, size_inclusions};
Point(13) = {125, -125, 0, size_inclusions};
Point(14) = {25, -125, 0, size_inclusions};
Point(15) = {225, -125, 0, size_inclusions};
Point(16) = {125, -125, 300, size_inclusions};
Point(17) = {25, -125, 300, size_inclusions};
Point(18) = {225, -125, 300, size_inclusions};
Point(19) = {125, 125, 0, size_holes};
Point(20) = {25, 125, 0, size_holes};
Point(21) = {225, 125, 0, size_holes};
Point(22) = {125, 125, 300, size_holes};
Point(23) = {25, 125, 300, size_holes};
Point(24) = {225, 125, 300, size_holes};
Point(25) = {-250.0, 250.0, 0, size_bulk};
Point(26) = {-250.0, -250.0, 0, size_bulk};
Point(27) = {250.0, 250.0, 0, size_bulk};
Point(28) = {250.0, -250.0, 0, size_bulk};
Point(29) = {-250.0, 250.0, 300, size_bulk};
Point(30) = {-250.0, -250.0, 300, size_bulk};
Point(31) = {250.0, 250.0, 300, size_bulk};
Point(32) = {250.0, -250.0, 300, size_bulk};

Circle(1) = {5, 4, 6};
Circle(2) = {2, 1, 3};
Circle(3) = {6, 4, 5};
Circle(4) = {3, 1, 2};
Line(5) = {2, 5};
Line(6) = {3, 6};
Line Loop(7) = {2, 6, -1, -5};
Line Loop(8) = {4, 5, -3, -6};
Ruled Surface(9) = {7};
Ruled Surface(10) = {8};
Circle(11) = {11, 10, 12};
Circle(12) = {8, 7, 9};
Circle(13) = {12, 10, 11};
Circle(14) = {9, 7, 8};
Line(15) = {8, 11};
Line(16) = {9, 12};
Line Loop(17) = {12, 16, -11, -15};
Line Loop(18) = {14, 15, -13, -16};
Ruled Surface(19) = {17};
Ruled Surface(20) = {18};
Circle(21) = {17, 16, 18};
Circle(22) = {14, 13, 15};
Circle(23) = {18, 16, 17};
Circle(24) = {15, 13, 14};
Line(25) = {14, 17};
Line(26) = {15, 18};
Line Loop(27) = {22, 26, -21, -25};
Line Loop(28) = {24, 25, -23, -26};
Ruled Surface(29) = {27};
Ruled Surface(30) = {28};
Circle(31) = {23, 22, 24};
Circle(32) = {20, 19, 21};
Circle(33) = {24, 22, 23};
Circle(34) = {21, 19, 20};
Line(35) = {20, 23};
Line(36) = {21, 24};
Line Loop(37) = {32, 36, -31, -35};
Line Loop(38) = {34, 35, -33, -36};
Ruled Surface(39) = {37};
Ruled Surface(40) = {38};
Line(41) = {26, 25};
Line(42) = {25, 27};
Line(43) = {27, 28};
Line(44) = {28, 26};
Line(45) = {30, 29};
Line(46) = {29, 31};
Line(47) = {31, 32};
Line(48) = {32, 30};
Line(49) = {26, 30};
Line(50) = {25, 29};
Line(51) = {27, 31};
Line(52) = {28, 32};
Line Loop(53) = {49, 45, -50, -41};
Line Loop(54) = {52, 48, -49, -44};
Line Loop(55) = {51, 47, -52, -43};
Line Loop(56) = {42, 51, -46, -50};
Plane Surface(57) = {53};
Plane Surface(58) = {54};
Plane Surface(59) = {55};
Plane Surface(60) = {56};
Line Loop(61) = {45, 46, 47, 48, -1, -3, -11, -13, -21, -23, -31, -33};
Line Loop(62) = {41, 42, 43, 44, -2, -4, -12, -14, -22, -24, -32, -34};
Plane Surface(63) = {61};
Plane Surface(64) = {62};
Surface Loop(65) = {57, 58, 59, 60, 63, 64, -9, -10, -19, -20, -29, -30, -39, -40};
Volume(66) = {65};
Line Loop(67) = {1, 3};
Plane Surface(68) = {67};
Line Loop(69) = {2, 4};
Plane Surface(70) = {69};
Surface Loop(71) = {9, 10, 68, 70};
Volume(72) = {71};
Line Loop(73) = {11, 13};
Plane Surface(74) = {73};
Line Loop(75) = {12, 14};
Plane Surface(76) = {75};
Surface Loop(77) = {19, 20, 74, 76};
Volume(78) = {77};
Line Loop(79) = {21, 23};
Plane Surface(80) = {79};
Line Loop(81) = {22, 24};
Plane Surface(82) = {81};
Surface Loop(83) = {29, 30, 80, 82};
Volume(84) = {83};

Physical Volume("mat1") = {66};
Physical Volume("mat2") = {72, 78, 84};