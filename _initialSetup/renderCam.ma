//Maya ASCII 2020 scene
//Name: renderCam.ma
//Last modified: Tue, Sep 08, 2020 12:08:01 AM
//Codeset: 1252
requires maya "2020";
requires -nodeType "displayPoints" "Type" "2.0a";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "4.0.2";
requires "stereoCamera" "10.0";
requires "Mayatomr" "2013.0 - 3.10.1.4 ";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "202004291615-7bd99f0972";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 18362)\n";
fileInfo "UUID" "9BBE8D8C-4F03-B0ED-4340-DEBCDD20FA41";
createNode transform -s -n "persp";
	rename -uid "672B9942-4CD0-077A-3F71-2F8AF43F7C89";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 23.073966936937055 9.4430260536606596 -4.2922172800703704 ;
	setAttr ".r" -type "double3" -21.938352729432438 99.799999999975455 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "AE1CCF49-4919-D847-8F74-7EB98F6D748D";
	setAttr -k off ".v" no;
	setAttr ".pze" yes;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 26.182290606304704;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 1.2212453270876722e-15 9.8371183519539062e-18 -0.45749865700385262 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "C76EED16-45DD-5CA3-0AFB-66AC8AC04F26";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "1B4CCA08-417A-F4AB-20B0-84937DB89098";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "12A5F732-4CBD-4CA5-70D6-EB8E17CE8C64";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "E307BBF6-476B-0777-FE9D-D09097A87E85";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "23C19676-4CD1-584C-54A3-F58F420058E4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3DFB4714-4F84-C03B-9316-E5BF49AE5DD8";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "cam_master_CTRL_GRP";
	rename -uid "D56CC0DE-4264-9B7B-F8DB-84AE2BE9DA48";
createNode transform -n "cam_master_CTRL" -p "cam_master_CTRL_GRP";
	rename -uid "4B55E361-4476-1632-5B39-F8AEB15CE56C";
	addAttr -ci true -k true -sn "rot_order" -ln "rot_order" -nn "rotation_order" -dv 
		5 -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" -at "enum";
	addAttr -ci true -k true -sn "__vis_Attrs__" -ln "__vis_Attrs__" -nn "__vis_Attrs__" 
		-min 0 -max 0 -en "-----" -at "enum";
	addAttr -ci true -sn "rot_and_trans_ctrl" -ln "rot_and_trans_ctrl" -min 0 -max 1 
		-at "bool";
	addAttr -ci true -sn "aim_ctrl" -ln "aim_ctrl" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "focus_ctrl" -ln "focus_ctrl" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "display_frustrums" -ln "display_frustrums" -min 0 -max 1 -at "bool";
	addAttr -ci true -k true -sn "__xtra_Attrs__" -ln "__xtra_Attrs__" -nn "__xtra_Attrs__" 
		-min 0 -max 0 -en "-----" -at "enum";
	addAttr -ci true -k true -sn "aim_on" -ln "aim_on" -min 0 -max 1 -at "float";
	addAttr -ci true -k true -sn "__cam_Attrs__" -ln "__cam_Attrs__" -nn "__cam_Attrs__" 
		-min 0 -max 0 -en "-----" -at "enum";
	addAttr -ci true -sn "horiz_aperture_inch" -ln "horiz_aperture_inch" -dv 1.417 -min 
		0 -max 5 -at "double";
	addAttr -ci true -sn "vert_aperture_inch" -ln "vert_aperture_inch" -dv 0.945 -min 
		0 -max 5 -at "double";
	addAttr -ci true -sn "focal_length" -ln "focal_length" -dv 35 -min 2 -at "double";
	addAttr -ci true -sn "near_clip" -ln "near_clip" -dv 1 -min 0.001 -max 1000000 -at "double";
	addAttr -ci true -sn "far_clip" -ln "far_clip" -dv 100000 -min 1 -max 1000000000 
		-at "double";
	addAttr -ci true -sn "fstop" -ln "fstop" -dv 5.6 -min 0.01 -max 22 -at "double";
	addAttr -ci true -sn "focus_region_scale" -ln "focus_region_scale" -dv 1 -min 0.01 
		-max 10 -at "double";
	addAttr -ci true -sn "shutter_angle" -ln "shutter_angle" -dv 144 -min 0 -max 360 
		-at "double";
	addAttr -ci true -sn "film_offset_x" -ln "film_offset_x" -min -5 -max 5 -at "double";
	addAttr -ci true -sn "film_offset_y" -ln "film_offset_y" -min -5 -max 5 -at "double";
	addAttr -ci true -sn "ai_exposure" -ln "ai_exposure" -min -10 -max 10 -at "double";
	addAttr -ci true -sn "ai_enable_dof" -ln "ai_enable_dof" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "ai_focal_distance" -ln "ai_focal_distance" -at "double";
	addAttr -ci true -sn "ai_aperture_size" -ln "ai_aperture_size" -min 0 -max 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".smd" 7;
	setAttr -k on ".rot_order";
	setAttr -k on ".rot_and_trans_ctrl";
	setAttr -k on ".aim_ctrl";
	setAttr -k on ".focus_ctrl";
	setAttr -k on ".display_frustrums";
	setAttr -l on -k on ".__xtra_Attrs__";
	setAttr -k on ".aim_on";
	setAttr -l on -k on ".__cam_Attrs__";
	setAttr -l on -k on ".horiz_aperture_inch";
	setAttr -l on -k on ".vert_aperture_inch";
	setAttr -k on ".focal_length";
	setAttr -k on ".near_clip" 2;
	setAttr -k on ".far_clip" 1000;
	setAttr -k on ".fstop";
	setAttr -k on ".focus_region_scale";
	setAttr -k on ".shutter_angle";
	setAttr -k on ".film_offset_x";
	setAttr -k on ".film_offset_y";
	setAttr -k on ".ai_exposure";
	setAttr -k on ".ai_enable_dof";
	setAttr -k on ".ai_focal_distance";
	setAttr -k on ".ai_aperture_size";
createNode nurbsCurve -n "cam_master_CTRLShape" -p "cam_master_CTRL";
	rename -uid "FEFCB384-4555-2775-78BD-A98790BF49E9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 11 0 no 3
		12 0 1 2 3 4 5 6 7 8 9 10 11
		12
		-1.5897965773285128 -3.4316863457212294e-16 1.9841670509765481
		-1.589796577328513 -3.4316863457212294e-16 -1.1280515356906955
		-0.32595171323962557 3.3720974738400762e-17 -1.1279628737279601
		-0.32596769058203739 -1.9071736946186498e-16 -1.9568405297515805
		-0.72229099806106511 -2.7871882169362735e-16 -1.9568405297515805
		-1.1413794146208324e-15 -1.1833800238825162e-16 -2.8991643649842542
		0.72229099806106578 4.2042816917124371e-17 -1.9568405297515805
		0.32492439839050941 -4.6190292717127457e-17 -1.9568405297515805
		0.32472438403681314 1.7820009169230908e-16 -1.1279628737279597
		1.5897965773285154 3.6284287127603075e-16 -1.1280515356906955
		1.5897965773285145 3.6284287127603075e-16 1.984167050976549
		-1.5897965773285128 -3.4316863457212294e-16 1.9841670509765481
		;
createNode transform -n "cam_offset_GRP" -p "cam_master_CTRL";
	rename -uid "4A445EA8-42FC-34AE-91C3-40AB718886C7";
createNode transform -n "offset_world_GRP" -p "cam_offset_GRP";
	rename -uid "AD0A768B-4DB5-A7A6-C3F9-F895E6316526";
createNode transform -n "offset_world" -p "offset_world_GRP";
	rename -uid "A077F18E-4A7F-1B15-C516-0381FEB3CEFD";
	addAttr -ci true -k true -sn "rot_order" -ln "rot_order" -nn "rotation_order" -dv 
		5 -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" -at "enum";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".sz";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sx";
	setAttr -k on ".rot_order";
createNode nurbsCurve -n "default3Shape" -p "offset_world";
	rename -uid "6FD4A03C-46B5-83B6-C82D-1FB5B110D932";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr ".cc" -type "nurbsCurve" 
		1 26 0 no 3
		27 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
		27
		3.9463811665422745e-16 -8.7062205836329391e-17 1.9110622175812129
		-0.41909280912230756 -1.7625156771034877e-16 1.8478941063730354
		-0.80094739527348935 -2.497802149958956e-16 1.6640026255190512
		-1.1116343473610319 -3.0111480572526343e-16 1.3757273377531682
		-1.3235476333747327 -3.2569400581454517e-16 1.0086827420389104
		-1.4178579670612343 -3.2133387883115138e-16 0.59548231600961632
		-1.386185307537902 -2.8842180589670231e-16 0.17284080551189007
		-1.2313440474916877 -2.2988219963391613e-16 -0.22168827255099538
		-0.98162947352411312 -1.5318507976320134e-16 -0.56871647593937125
		-0.626183685937724 -5.9421286608257485e-17 -0.81105527152364432
		-0.201759681396005 4.1290137256951543e-17 -0.91672436493891263
		-0.2016799358933668 -1.0818027873122997e-16 -1.3752789274285515
		-0.43607954912002667 -1.602274482447239e-16 -1.3752789274285517
		-9.8659529163556874e-16 -6.3398337044481979e-17 -1.9442021928387869
		0.43607954912002594 3.3430774155760256e-17 -1.375278927428552
		0.20167993589336597 -1.8616395357733676e-17 -1.3752789274285522
		0.19972895623507039 1.3043852318163277e-16 -0.91672436493891296
		0.6169104870398544 2.1542197675853901e-16 -0.7917992796429334
		0.96709249841559397 2.7855878385453547e-16 -0.55304930296662236
		1.2498532409636098 3.2170861438323769e-16 -0.23237455777071342
		1.4070220170673544 3.3208602131113254e-16 0.16808496578138876
		1.4178579670612335 3.0832154544068848e-16 0.5954823160096161
		1.3235476333747327 2.6207921688976023e-16 1.0086827420389104
		1.1116343473610319 1.9255001323648736e-16 1.3757273377531662
		0.80094739527348857 1.0591188090257412e-16 1.6640026255190508
		0.41909280912230645 9.8630267466197906e-18 1.8478941063730345
		3.9463811665422745e-16 -8.7062205836329391e-17 1.9110622175812129
		;
createNode transform -n "aim_GRP" -p "offset_world";
	rename -uid "F32558CE-49E2-14B0-6B27-BBB31BF0BE06";
createNode transform -n "rotation_CTRL_GRP" -p "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP";
	rename -uid "154EDF3C-4B22-F9BF-DF30-B4B13F18A66B";
	addAttr -ci true -k true -sn "rot_order" -ln "rot_order" -nn "rotation_order" -dv 
		5 -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" -at "enum";
	setAttr -k on ".rot_order";
createNode transform -n "rotation_CTRL" -p "rotation_CTRL_GRP";
	rename -uid "358DDFAE-4B5F-D6F9-5C53-249F583EBF75";
	addAttr -ci true -k true -sn "rot_order" -ln "rot_order" -nn "rotation_order" -dv 
		5 -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" -at "enum";
	setAttr -l on -k off ".v";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on -k off ".sz";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sx";
	setAttr -k on ".rot_order";
createNode nurbsCurve -n "rotation_CTRLShape" -p "rotation_CTRL";
	rename -uid "0EF588DB-4F89-9389-7178-3DBA7BB0F65B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".cc" -type "nurbsCurve" 
		1 57 0 no 3
		58 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57
		58
		0.18088221859450107 1.3184744815117286 0.18088221859450077
		0.18088221859450107 1.3184744815117286 0.18088221859450077
		0.28422619324547166 1.2966286338676225 0.18088221859450077
		0.4428395595030869 1.215248175861821 0.18088221859450077
		0.57369558666561948 1.1071071607816338 0.18088221859450077
		0.72352887437800362 0.95594579080509412 0.18088221859450077
		0.72352887437800406 0.97314091396417202 0.095711977221574596
		0.72352887437800339 0.97920584733790972 -0.031178715784517946
		0.72352887437800362 0.95594579080509412 -0.18088221859450077
		0.63714093316866582 1.0451762667402147 -0.18088221859450077
		0.47059689859816944 1.1950535283059711 -0.18088221859450077
		0.33577553727919623 1.2767525493459788 -0.18088221859450077
		0.18088221859450107 1.3184744815117286 -0.18088221859450077
		0.062167480484810182 1.3225908468744816 -0.18088221859450077
		-0.072653880834162687 1.3226641183908854 -0.18088221859450077
		-0.18088221859450102 1.3184744815117286 -0.18088221859450077
		-0.30660859606414509 1.2887769444237509 -0.18088221859450077
		-0.46522196232176044 1.199091441617371 -0.18088221859450077
		-0.58021665285853152 1.1009637259067888 -0.18088221859450077
		-0.72352887437800406 0.95594579080509412 -0.18088221859450077
		-0.72352887437800362 0.97620433566432974 -0.070832057348921604
		-0.72352887437800362 0.9747184166377707 0.08381597475225333
		-0.72352887437800406 0.95594579080509412 0.18088221859450077
		-0.61193932611005464 1.0703088203849538 0.18088221859450077
		-0.45332595985243934 1.207812337480064 0.18088221859450077
		-0.31850459853346647 1.2841192464649054 0.18088221859450077
		-0.18088221859450102 1.3184744815117286 0.18088221859450077
		-0.060757878364841679 1.3225792548360167 0.18088221859450077
		0.097855487892773721 1.3226696271188172 0.18088221859450077
		0.18088221859450107 1.3184744815117286 0.18088221859450077
		0.18088221859450124 1.3226805802970618 0.075885306439372385
		0.18088221859450096 1.3227014136658886 -0.090658728131123703
		0.18088221859450107 1.3184744815117286 -0.18088221859450077
		0.18088221859450107 1.295078110219628 -0.28892543595314302
		0.18088221859450107 1.2357972699365731 -0.4118507948027948
		0.18088221859450107 1.1138184371301048 -0.56649882690396958
		0.18088221859450102 0.95594579080509456 -0.72352887437800306
		0.078028817110571719 0.97541120540189374 -0.72352887437800306
		-0.048861875895520414 0.97815439581458818 -0.72352887437800306
		-0.18088221859450085 0.95594579080509479 -0.72352887437800306
		-0.18088221859450102 1.0951569816089302 -0.58632549768617159
		-0.18088221859450085 1.2307448156309659 -0.41978146311567549
		-0.1808822185945009 1.2963898850671574 -0.28496010179670261
		-0.18088221859450102 1.3184744815117286 -0.18088221859450077
		-0.18088221859450071 1.3226533846388238 -0.070832057348921604
		-0.1808822185945009 1.322704313990223 0.08381597475225333
		-0.18088221859450102 1.3184744815117286 0.18088221859450077
		-0.18088221859450077 1.2875452041397804 0.30984002166935504
		-0.18088221859450107 1.2083404890944085 0.45259205130120872
		-0.18088221859450085 1.0788001555785103 0.60327474924594338
		-0.18088221859450085 0.95594579080509479 0.72352887437800306
		-0.084549883303484008 0.97462706291663692 0.72352887437800306
		0.066132814641250565 0.97668120148185178 0.72352887437800306
		0.18088221859450102 0.95594579080509456 0.72352887437800306
		0.1808822185945009 1.0749244267834808 0.60724008340238356
		0.18088221859450107 1.2025722483068342 0.46052271961408991
		0.18088221859450115 1.2919569663633568 0.29794401920003405
		0.18088221859450107 1.3184744815117286 0.18088221859450077
		;
createNode transform -n "translation_local_CTRL_GRP" -p "rotation_CTRL";
	rename -uid "1203AAEF-4F0C-7C08-111B-D2971D7DD0E0";
createNode transform -n "translation_local_CTRL" -p "translation_local_CTRL_GRP";
	rename -uid "04816DC9-4ACE-B76B-F664-7BB8EDE828E0";
	addAttr -ci true -k true -sn "rot_order" -ln "rot_order" -nn "rotation_order" -dv 
		5 -min 0 -max 5 -en "xyz:yzx:zxy:xzy:yxz:zyx" -at "enum";
	setAttr -l on -k off ".v";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on -k off ".sz";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sx";
	setAttr -k on ".rot_order";
createNode nurbsCurve -n "translation_local_CTRLShape" -p "translation_local_CTRL";
	rename -uid "4ED66F2D-466D-47AA-9102-BFBCE0EDAF81";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32
		33
		0.87438161408372439 0.32848840028609799 -0.87415795664533724
		0.87529098963317331 0.32848840028609805 -0.17927211019816816
		1.3311703173106992 0.32848840028609783 -0.17928091135383806
		1.3311703173106992 0.32848840028609783 -0.39725710725151081
		1.8494445888765678 0.32848840028609771 2.236383738207103e-16
		1.3311703173106992 0.32848840028609783 0.39725710725151081
		1.3311703173106992 0.32848840028609783 0.17870709916508823
		0.87529098963317331 0.32848840028609805 0.17859708471921298
		0.87415795664533724 0.32848840028609799 0.87438161408372439
		0.17927211019816816 0.32848840028609821 0.87529098963317331
		0.17928091135383806 0.32848840028609805 1.3311703173106992
		0.39725710725151081 0.32848840028609805 1.3311703173106992
		5.9768001231495826e-16 0.3284884002860981 1.8494445888765678
		-0.39725710725151081 0.32848840028609821 1.3311703173106992
		-0.17870709916508823 0.32848840028609816 1.3311703173106992
		-0.17859708471921298 0.32848840028609827 0.87529098963317331
		-0.87438161408372439 0.32848840028609838 0.87533978200495799
		-0.87529098963317331 0.32848840028609844 0.17927211019816816
		-1.3311703173106992 0.32848840028609838 0.17928091135383806
		-1.3311703173106992 0.32848840028609838 0.39725710725151081
		-1.8494445888765678 0.32848840028609849 1.4189983984506274e-15
		-1.3311703173106992 0.32848840028609838 -0.39725710725151081
		-1.3311703173106992 0.32848840028609838 -0.17870709916508823
		-0.87529098963317331 0.32848840028609844 -0.17859708471921298
		-0.87438161408372439 0.32848840028609838 -0.87533978200495799
		-0.17927211019816816 0.32848840028609827 -0.87529098963317331
		-0.17928091135383806 0.32848840028609816 -1.3311703173106992
		-0.39725710725151081 0.32848840028609821 -1.3311703173106992
		1.2714483375121957e-15 0.3284884002860981 -1.8494445888765678
		0.39725710725151081 0.32848840028609805 -1.3311703173106992
		0.17870709916508823 0.32848840028609805 -1.3311703173106992
		0.17859708471921298 0.32848840028609821 -0.87529098963317331
		0.87438161408372439 0.32848840028609799 -0.87415795664533724
		;
createNode transform -n "nodelOffset_GRP" -p "translation_local_CTRL";
	rename -uid "E5DF5404-4B8A-BE1D-B5A1-78B218613498";
createNode transform -n "renderCam" -p "nodelOffset_GRP";
	rename -uid "76ED9743-43CB-6E47-2FDA-3BAAF350D240";
	setAttr -l on ".v";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode camera -n "renderCamShape" -p "renderCam";
	rename -uid "E50C5D1E-43BE-AC07-CDD4-B3AE329ACE92";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 1;
	setAttr ".rnd" no;
	setAttr ".ff" 0;
	setAttr ".ovr" 1.3;
	setAttr ".ncp" 2;
	setAttr ".fcp" 1000;
	setAttr ".coi" 15.185677880132999;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "camera1";
	setAttr ".den" -type "string" "camera1_depth";
	setAttr ".man" -type "string" "camera1_mask";
	setAttr ".dr" yes;
	setAttr ".ai_translator" -type "string" "perspective";
createNode aimConstraint -n "aim_GRP_aimConstraint1" -p "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP";
	rename -uid "0A4A01AE-414F-DA45-F86E-3C9DF0D72E72";
	addAttr -dcb 0 -ci true -sn "w0" -ln "aim_CTRLW0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" 0 0 -1 ;
	setAttr ".wut" 1;
	setAttr -k on ".w0";
createNode transform -n "aim_GRP" -p "cam_master_CTRL_GRP";
	rename -uid "8D25C555-4794-56D8-5507-24B7E632995C";
createNode transform -n "aim_CTRL_GRP" -p "|cam_master_CTRL_GRP|aim_GRP";
	rename -uid "EE5676D9-4746-372A-1E17-E3881A17DE00";
	setAttr ".t" -type "double3" 0 0 -6.312191484049368 ;
createNode transform -n "aim_CTRL" -p "aim_CTRL_GRP";
	rename -uid "3A88C0E1-470D-D11E-8403-57B9091531A9";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "aim_CTRLShape" -p "aim_CTRL";
	rename -uid "BBD74003-4614-F72B-FF81-C4B836790833";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".cc" -type "nurbsCurve" 
		1 52 0 no 3
		53 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52
		53
		-0.12091105991418938 0 0
		-0.11170731003352129 -0.046270607141141736 0
		-0.085497056842742725 -0.085497056842742725 0
		-0.046270607141141736 -0.11170731003352129 0
		0 -0.12091105991418938 0
		0.046270607141141736 -0.11170731003352129 0
		0.085497056842742725 -0.085497056842742725 0
		0.11170731003352129 -0.046270607141141736 0
		0.12091105991418938 0 0
		0.11170731003352129 0.046270607141141736 0
		0.085497056842742725 0.085497056842742725 0
		0.046270607141141736 0.11170731003352129 0
		0 0.12091105991418938 0
		-0.046270607141141736 0.11170731003352129 0
		-0.085497056842742725 0.085497056842742725 0
		-0.11170731003352129 0.046270607141141736 0
		-0.12091105991418938 0 0
		-0.11170731003352129 0 0.046270607141141736
		-0.085497056842742725 0 0.085497056842742725
		-0.046270607141141736 0 0.11170731003352129
		0 0 0.12091105991418938
		0.046270607141141736 0 0.11170731003352129
		0.085497056842742725 0 0.085497056842742725
		0.11170731003352129 0 0.046270607141141736
		0.12091105991418938 0 0
		0.11170731003352129 0 -0.046270607141141736
		0.085497056842742725 0 -0.085497056842742725
		0.046270607141141736 0 -0.11170731003352129
		0 0 -0.12091105991418938
		-0.046270607141141736 0 -0.11170731003352129
		-0.085497056842742725 0 -0.085497056842742725
		-0.11170731003352129 0 -0.046270607141141736
		-0.12091105991418938 0 0
		-0.11170731003352129 -0.046270607141141736 0
		-0.085497056842742725 -0.085497056842742725 0
		-0.046270607141141736 -0.11170731003352129 0
		0 -0.12091105991418938 0
		0 -0.11170731003352129 0.046270607141141736
		0 -0.085497056842742725 0.085497056842742725
		0 -0.046270607141141736 0.11170731003352129
		0 0 0.12091105991418938
		0 0.046270607141141736 0.11170731003352129
		0 0.085497056842742725 0.085497056842742725
		0 0.11170731003352129 0.046270607141141736
		0 0.12091105991418938 0
		0 0.11170731003352129 -0.046270607141141736
		0 0.085497056842742725 -0.085497056842742725
		0 0.046270607141141736 -0.11170731003352129
		0 0 -0.12091105991418938
		0 -0.046270607141141736 -0.11170731003352129
		0 -0.085497056842742725 -0.085497056842742725
		0 -0.11170731003352129 -0.046270607141141736
		0 -0.12091105991418938 0
		;
createNode transform -n "up_CTRL_GRP" -p "|cam_master_CTRL_GRP|aim_GRP";
	rename -uid "47466E7D-45EB-84F1-4A8E-92B2115E2904";
createNode transform -n "aimUp_CTRL" -p "up_CTRL_GRP";
	rename -uid "A6DE4297-4F7A-298A-3A4E-318780CBF6A5";
	addAttr -ci true -k true -sn "__xtraAttrs__" -ln "__xtraAttrs__" -nn "__xtraAttrs__" 
		-min 0 -max 0 -en "-----" -at "enum";
	addAttr -ci true -sn "follow_offset_world" -ln "follow_offset_world" -min 0 -max 
		1 -at "bool";
	setAttr -l on -k on ".__xtraAttrs__";
	setAttr -k on ".follow_offset_world" yes;
createNode nurbsCurve -n "aimUp_CTRLShape" -p "aimUp_CTRL";
	rename -uid "EC01760D-4791-9A33-F516-30AEC2A3C1A4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 2 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-0.01824493625112774 0.044047172542103649 -1.1171801390295079e-18
		-3.6676127196050777e-17 0.15470856116783049 -2.2457650887882387e-33
		0.018244936251126744 0.044047172542103649 1.1171801390295045e-18
		0.10939547270938675 0.10939547270938675 6.6985407747381063e-18
		0.044047172542103663 0.018244936251126744 2.6971114432589271e-18
		0.15470856116783055 -7.1363323940590063e-18 9.4731672117438091e-18
		0.04404717254210299 -0.018244936251127417 2.6971114432589271e-18
		0.10939547270938675 -0.10939547270938681 6.6985407747381063e-18
		0.01824493625112673 -0.044047172542103649 1.1171801390295045e-18
		-1.1691275137825554e-17 -0.15470856116783049 -7.1588413377445475e-34
		-0.01824493625112774 -0.044047172542103649 -1.1171801390295079e-18
		-0.10939547270938675 -0.10939547270938672 -6.6985407747381056e-18
		-0.044047172542103545 -0.01824493625112741 -2.697111443258934e-18
		-0.15470856116783047 2.657815823370564e-17 -9.4731672117438075e-18
		-0.044047172542103642 0.018244936251126755 -2.697111443258934e-18
		-0.10939547270938672 0.10939547270938677 -6.6985407747381033e-18
		-0.01824493625112774 0.044047172542103649 -1.1171801390295079e-18
		;
createNode parentConstraint -n "up_CTRL_GRP_parentConstraint1" -p "up_CTRL_GRP";
	rename -uid "FFFEE421-4E7E-B907-4340-2699128D4172";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "offset_worldW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 0 5.7503993141587646 0 ;
	setAttr ".lr" -type "double3" -8.0040989872046335 33.70441632226435 -0.96342283623554315 ;
	setAttr ".rst" -type "double3" 0 5.7503993141587646 0 ;
	setAttr -k on ".w0";
createNode transform -n "focus_CTRL_GRP" -p "cam_master_CTRL_GRP";
	rename -uid "CEE2897D-4735-2AC4-CD74-16BB968EB729";
createNode transform -n "focus_CTRL" -p "focus_CTRL_GRP";
	rename -uid "4E6973BA-4F37-F7AB-1FE0-BCA50A674EBA";
	addAttr -ci true -k true -sn "__xtraAttrs__" -ln "__xtraAttrs__" -nn "__xtraAttrs__" 
		-min 0 -max 0 -en "-----" -at "enum";
	addAttr -ci true -sn "follow_camera" -ln "follow_camera" -min 0 -max 1 -at "bool";
	setAttr -l on -k off ".v";
	setAttr ".t" -type "double3" 0 0 5 ;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -l on -k on ".__xtraAttrs__";
	setAttr -k on ".follow_camera" yes;
createNode nurbsCurve -n "focus_CTRLShape" -p "focus_CTRL";
	rename -uid "D335F211-4296-C969-D6EE-7C9128300C63";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 14 0 no 3
		15 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
		15
		-0.10053100888055741 0 -0.10053100888055741
		-0.10053100888055741 0 0.10053100888055741
		0.10053100888055741 0 0.10053100888055741
		0.10053100888055741 0 -0.10053100888055741
		-0.10053100888055741 0 -0.10053100888055741
		0 0.20106201776111482 0
		-0.10053100888055741 0 0.10053100888055741
		0.10053100888055741 0 0.10053100888055741
		0 0.20106201776111482 0
		0.10053100888055741 0 -0.10053100888055741
		-2.4622996722557243e-17 -0.20106201776111482 0
		-0.10053100888055741 0 -0.10053100888055741
		-0.10053100888055741 0 0.10053100888055741
		-2.4622996722557243e-17 -0.20106201776111482 0
		0.10053100888055741 0 0.10053100888055741
		;
createNode parentConstraint -n "focus_CTRL_GRP_parentConstraint1" -p "focus_CTRL_GRP";
	rename -uid "A78216C6-40E0-7325-41AA-3EA523F84A51";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "renderCamW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tor" -type "double3" 0 179.99999999999994 0 ;
	setAttr ".lr" -type "double3" 0 179.99999999999994 0 ;
	setAttr ".rsrr" -type "double3" 0 179.99999999999994 0 ;
	setAttr -k on ".w0";
createNode transform -n "transform1";
	rename -uid "8FA510BC-4B28-1D4A-E845-8FB553B5326C";
	setAttr ".hio" yes;
createNode displayPoints -n "displayPoints1" -p "transform1";
	rename -uid "6C89CFEE-41C6-668D-2A7C-CB8DC90E6637";
	setAttr -k off ".v";
	setAttr ".hio" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "261701A4-492F-1362-4327-A2AEE8C69ADE";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "F379B287-46BB-0DE6-9967-F4B42043246D";
	setAttr -s 2 ".dli[1]"  1;
	setAttr -s 2 ".dli";
createNode displayLayer -n "defaultLayer";
	rename -uid "465A27F0-42E1-717F-1C5C-DF8C7A3745B5";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "50BAC0A2-404D-F421-955D-4D9761BC686F";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "1884F435-446C-0EC8-44E2-AE94327E1ADF";
	setAttr ".g" yes;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "8325129B-4A0A-CAC0-BA8F-4B92F924153D";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "C1565154-4F66-206C-AF24-AE935B31489E";
createNode blinn -n "typeBlinn";
	rename -uid "52316326-4239-0C27-6E26-A1816EBE1B6E";
	setAttr ".c" -type "float3" 1 1 1 ;
createNode shadingEngine -n "typeBlinnSG";
	rename -uid "162168EC-48EF-3C39-DC2A-C6BFC1FD0360";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo1";
	rename -uid "C1B518B4-49F9-3889-0B72-31A67473F236";
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "2C4649AE-4F9B-E1D6-9D0B-C9B26A8BA3F7";
	setAttr ".AA_samples" 8;
	setAttr ".enable_adaptive_sampling" yes;
	setAttr ".rndrdvc" 1;
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "D14F2E2F-4FB9-3F0E-6101-D0BECDDB2E0C";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "A4DE1C16-4CA8-4017-7ED3-928F663F2BB1";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "3B7C1DF7-4564-B599-C166-AAA28F201BBE";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode unitConversion -n "unitConversion1";
	rename -uid "DBD425A3-4421-10B9-C7D1-1D8C8D72FD19";
	setAttr ".cf" 0.017453292519943295;
createNode displayLayer -n "auto_DL";
	rename -uid "0B816126-49C8-9B37-9AA7-CCAB6EA9A0A9";
	setAttr ".dt" 2;
	setAttr ".do" 1;
createNode distanceBetween -n "distanceBetween1";
	rename -uid "F6F52A3A-45FC-9D67-A693-FE912685E6F8";
createNode decomposeMatrix -n "focus_DM";
	rename -uid "11A8293E-40A4-7164-79D8-32B6745140BF";
createNode decomposeMatrix -n "cam_DM";
	rename -uid "DF7D7515-4704-A435-3498-94AB8A54F857";
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "D623BC2A-445D-F8DB-6181-0F8570090435";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "0E2AB4F5-45AA-EF35-4E04-AA90370E2DDB";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 789\n            -height 352\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 789\n            -height 352\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n"
		+ "            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1585\n            -height 748\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"renderCam\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n"
		+ "            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n"
		+ "            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n"
		+ "            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 789\n            -height 748\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n"
		+ "            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n"
		+ "            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n"
		+ "                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n"
		+ "                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n"
		+ "                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n"
		+ "\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n"
		+ "                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n"
		+ "                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n"
		+ "                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n"
		+ "                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n"
		+ "\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xC:/Golaem/GolaemCrowdCharacterPack-4.0.4/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Front View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Front View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"persp\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1585\\n    -height 748\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Front View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"persp\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1585\\n    -height 748\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "A64DFFD7-46DE-06A6-079E-17A96FBE6536";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 62.820282902673789 -1084.2517702238106 ;
	setAttr ".tgi[0].vh" -type "double2" 1718.1320272810206 107.41484909027935 ;
	setAttr -s 11 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 798.5714111328125;
	setAttr ".tgi[0].ni[0].y" 41.428569793701172;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 132.37464904785156;
	setAttr ".tgi[0].ni[1].y" -1032.5418701171875;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -122.21539306640625;
	setAttr ".tgi[0].ni[2].y" 282.67581176757813;
	setAttr ".tgi[0].ni[2].nvs" 1923;
	setAttr ".tgi[0].ni[3].x" 115.96639251708984;
	setAttr ".tgi[0].ni[3].y" 26.806718826293945;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 557.5675048828125;
	setAttr ".tgi[0].ni[4].y" -808.999755859375;
	setAttr ".tgi[0].ni[4].nvs" 18306;
	setAttr ".tgi[0].ni[5].x" 487.14285278320313;
	setAttr ".tgi[0].ni[5].y" 57.142856597900391;
	setAttr ".tgi[0].ni[5].nvs" 1923;
	setAttr ".tgi[0].ni[6].x" 418.57144165039063;
	setAttr ".tgi[0].ni[6].y" -404.28570556640625;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -127.14286041259766;
	setAttr ".tgi[0].ni[7].y" -54.285713195800781;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 180;
	setAttr ".tgi[0].ni[8].y" 47.142856597900391;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 180;
	setAttr ".tgi[0].ni[9].y" -54.285713195800781;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 1167.142822265625;
	setAttr ".tgi[0].ni[10].y" 2005.7142333984375;
	setAttr ".tgi[0].ni[10].nvs" 18306;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".outf" 51;
	setAttr ".imfkey" -type "string" "exr";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "cam_master_CTRL.rot_order" "cam_master_CTRL.ro";
connectAttr "distanceBetween1.d" "cam_master_CTRL.ai_focal_distance";
connectAttr "offset_world.rot_order" "offset_world.ro";
connectAttr "aim_GRP_aimConstraint1.crx" "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.rx"
		;
connectAttr "aim_GRP_aimConstraint1.cry" "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.ry"
		;
connectAttr "aim_GRP_aimConstraint1.crz" "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.rz"
		;
connectAttr "rotation_CTRL_GRP.rot_order" "rotation_CTRL_GRP.ro";
connectAttr "rotation_CTRL.rot_order" "rotation_CTRL.ro";
connectAttr "cam_master_CTRL.rot_and_trans_ctrl" "rotation_CTRLShape.v";
connectAttr "translation_local_CTRL.rot_order" "translation_local_CTRL.ro";
connectAttr "cam_master_CTRL.rot_and_trans_ctrl" "translation_local_CTRLShape.v"
		;
connectAttr "cam_master_CTRL.near_clip" "renderCamShape.ncp";
connectAttr "cam_master_CTRL.far_clip" "renderCamShape.fcp";
connectAttr "cam_master_CTRL.fstop" "renderCamShape.fs";
connectAttr "cam_master_CTRL.focal_length" "renderCamShape.fl";
connectAttr "cam_master_CTRL.focus_region_scale" "renderCamShape.frs";
connectAttr "cam_master_CTRL.ai_focal_distance" "renderCamShape.fd";
connectAttr "cam_master_CTRL.near_clip" "renderCamShape.ai_near_clip";
connectAttr "cam_master_CTRL.far_clip" "renderCamShape.ai_far_clip";
connectAttr "cam_master_CTRL.ai_focal_distance" "renderCamShape.ai_focus_distance"
		;
connectAttr "cam_master_CTRL.ai_enable_dof" "renderCamShape.ai_edof";
connectAttr "cam_master_CTRL.ai_exposure" "renderCamShape.ai_exposure";
connectAttr "cam_master_CTRL.film_offset_x" "renderCamShape.hfo";
connectAttr "cam_master_CTRL.film_offset_y" "renderCamShape.vfo";
connectAttr "cam_master_CTRL.horiz_aperture_inch" "renderCamShape.hfa";
connectAttr "cam_master_CTRL.vert_aperture_inch" "renderCamShape.vfa";
connectAttr "unitConversion1.o" "renderCamShape.sa";
connectAttr "cam_master_CTRL.display_frustrums" "renderCamShape.cnc";
connectAttr "cam_master_CTRL.display_frustrums" "renderCamShape.cfp";
connectAttr "cam_master_CTRL.display_frustrums" "renderCamShape.dcf";
connectAttr "cam_master_CTRL.ai_aperture_size" "renderCamShape.ai_aperture_size"
		;
connectAttr "cam_master_CTRL.aim_on" "aim_GRP_aimConstraint1.w0";
connectAttr "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.pim" "aim_GRP_aimConstraint1.cpim"
		;
connectAttr "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.t" "aim_GRP_aimConstraint1.ct"
		;
connectAttr "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.rp" "aim_GRP_aimConstraint1.crp"
		;
connectAttr "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.rpt" "aim_GRP_aimConstraint1.crt"
		;
connectAttr "|cam_master_CTRL_GRP|cam_master_CTRL|cam_offset_GRP|offset_world_GRP|offset_world|aim_GRP.ro" "aim_GRP_aimConstraint1.cro"
		;
connectAttr "aim_CTRL.t" "aim_GRP_aimConstraint1.tg[0].tt";
connectAttr "aim_CTRL.rp" "aim_GRP_aimConstraint1.tg[0].trp";
connectAttr "aim_CTRL.rpt" "aim_GRP_aimConstraint1.tg[0].trt";
connectAttr "aim_CTRL.pm" "aim_GRP_aimConstraint1.tg[0].tpm";
connectAttr "aim_GRP_aimConstraint1.w0" "aim_GRP_aimConstraint1.tg[0].tw";
connectAttr "aimUp_CTRL.wm" "aim_GRP_aimConstraint1.wum";
connectAttr "cam_master_CTRL.aim_ctrl" "|cam_master_CTRL_GRP|aim_GRP.v";
connectAttr "up_CTRL_GRP_parentConstraint1.ctx" "up_CTRL_GRP.tx";
connectAttr "up_CTRL_GRP_parentConstraint1.cty" "up_CTRL_GRP.ty";
connectAttr "up_CTRL_GRP_parentConstraint1.ctz" "up_CTRL_GRP.tz";
connectAttr "up_CTRL_GRP_parentConstraint1.crx" "up_CTRL_GRP.rx";
connectAttr "up_CTRL_GRP_parentConstraint1.cry" "up_CTRL_GRP.ry";
connectAttr "up_CTRL_GRP_parentConstraint1.crz" "up_CTRL_GRP.rz";
connectAttr "up_CTRL_GRP.ro" "up_CTRL_GRP_parentConstraint1.cro";
connectAttr "up_CTRL_GRP.pim" "up_CTRL_GRP_parentConstraint1.cpim";
connectAttr "up_CTRL_GRP.rp" "up_CTRL_GRP_parentConstraint1.crp";
connectAttr "up_CTRL_GRP.rpt" "up_CTRL_GRP_parentConstraint1.crt";
connectAttr "offset_world.t" "up_CTRL_GRP_parentConstraint1.tg[0].tt";
connectAttr "offset_world.rp" "up_CTRL_GRP_parentConstraint1.tg[0].trp";
connectAttr "offset_world.rpt" "up_CTRL_GRP_parentConstraint1.tg[0].trt";
connectAttr "offset_world.r" "up_CTRL_GRP_parentConstraint1.tg[0].tr";
connectAttr "offset_world.ro" "up_CTRL_GRP_parentConstraint1.tg[0].tro";
connectAttr "offset_world.s" "up_CTRL_GRP_parentConstraint1.tg[0].ts";
connectAttr "offset_world.pm" "up_CTRL_GRP_parentConstraint1.tg[0].tpm";
connectAttr "up_CTRL_GRP_parentConstraint1.w0" "up_CTRL_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "aimUp_CTRL.follow_offset_world" "up_CTRL_GRP_parentConstraint1.w0";
connectAttr "cam_master_CTRL.focus_ctrl" "focus_CTRL_GRP.v";
connectAttr "focus_CTRL_GRP_parentConstraint1.ctx" "focus_CTRL_GRP.tx";
connectAttr "focus_CTRL_GRP_parentConstraint1.cty" "focus_CTRL_GRP.ty";
connectAttr "focus_CTRL_GRP_parentConstraint1.ctz" "focus_CTRL_GRP.tz";
connectAttr "focus_CTRL_GRP_parentConstraint1.crx" "focus_CTRL_GRP.rx";
connectAttr "focus_CTRL_GRP_parentConstraint1.cry" "focus_CTRL_GRP.ry";
connectAttr "focus_CTRL_GRP_parentConstraint1.crz" "focus_CTRL_GRP.rz";
connectAttr "focus_CTRL_GRP.ro" "focus_CTRL_GRP_parentConstraint1.cro";
connectAttr "focus_CTRL_GRP.pim" "focus_CTRL_GRP_parentConstraint1.cpim";
connectAttr "focus_CTRL_GRP.rp" "focus_CTRL_GRP_parentConstraint1.crp";
connectAttr "focus_CTRL_GRP.rpt" "focus_CTRL_GRP_parentConstraint1.crt";
connectAttr "renderCam.t" "focus_CTRL_GRP_parentConstraint1.tg[0].tt";
connectAttr "renderCam.rp" "focus_CTRL_GRP_parentConstraint1.tg[0].trp";
connectAttr "renderCam.rpt" "focus_CTRL_GRP_parentConstraint1.tg[0].trt";
connectAttr "renderCam.r" "focus_CTRL_GRP_parentConstraint1.tg[0].tr";
connectAttr "renderCam.ro" "focus_CTRL_GRP_parentConstraint1.tg[0].tro";
connectAttr "renderCam.s" "focus_CTRL_GRP_parentConstraint1.tg[0].ts";
connectAttr "renderCam.pm" "focus_CTRL_GRP_parentConstraint1.tg[0].tpm";
connectAttr "focus_CTRL_GRP_parentConstraint1.w0" "focus_CTRL_GRP_parentConstraint1.tg[0].tw"
		;
connectAttr "focus_CTRL.follow_camera" "focus_CTRL_GRP_parentConstraint1.w0";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "typeBlinnSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "typeBlinnSG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "typeBlinn.oc" "typeBlinnSG.ss";
connectAttr "typeBlinnSG.msg" "materialInfo1.sg";
connectAttr "typeBlinn.msg" "materialInfo1.m";
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "cam_master_CTRL.shutter_angle" "unitConversion1.i";
connectAttr "layerManager.dli[1]" "auto_DL.id";
connectAttr "cam_DM.ot" "distanceBetween1.p2";
connectAttr "focus_DM.ot" "distanceBetween1.p1";
connectAttr "focus_CTRL.wm" "focus_DM.imat";
connectAttr "renderCam.wm" "cam_DM.imat";
connectAttr "sceneConfigurationScriptNode.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "renderCamShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn";
connectAttr "renderCam.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "focus_CTRLShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "cam_master_CTRL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "cam_master_CTRLShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "focus_CTRL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "cam_DM.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr "focus_DM.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "focus_CTRL_GRP_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "typeBlinnSG.pa" ":renderPartition.st" -na;
connectAttr "typeBlinn.msg" ":defaultShaderList1.s" -na;
connectAttr "distanceBetween1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of renderCam.ma
