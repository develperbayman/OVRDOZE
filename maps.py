from classtest import *
from values import *
import classes

mouse_conversion = fs_size[0] / size[0]

## mouse_conversion =  1920 / 854 = 2.25
## mouse_conversion =  2560 / 854 = 2.99


## 2.25^2/2.99

# 854x480


maps = [
    Map(
        "Overworld",
        "overworld.png",
        "nav_mesh_overworld.txt",
        [0, 0],
        mouse_conversion,
        [2500, 2500],
        POLYGONS=[  # x,y,width,height
            [2, 1503, 773, 553],
            [1501, 2259, 506, 239],
            [952, 1503, 550, 996],
            [2008, 1503, 492, 996],
            [828, 2, 1670, 744],
            [498, 685, 330, 57],
            [2, 685, 242, 57],
        ],
        OBJECTS=[
            classes.Interactable(
                [164, 30], None, name="Rupert", type="NPC", image="placeholder_npc.png"
            ),

            classes.Interactable(
                [495, 630], None, name="Alan", type="NPC", image="npc_alley.png", angle = 180
            ),

            classes.Interactable(
                [560, 330], None, name="Payphone", type="NPC", image="payphone.png"
            ),

            classes.Interactable(
                [782, 1005], None, name="Basement", type="door", door_dest="Liberation", active = False,
            ),
        ],
        SPAWNPOINT=[781, 930],
        GAMMA=[0.8, 0.9, 1.2],
        TOP_LAYER="overworld_top.png",
        NO_LOS_POLYGONS=[
            [52, 190, 657, 78],
            [503, 559, 320, 124],
            [722, 389, 106, 170],
        ],
    ),
    Map(
        "Requiem",
        "map.png",
        "nav_mesh_requiem.txt",
        [0, 0],
        mouse_conversion,
        [2000, 1500],
        POLYGONS=[
            [501, 0, 125, 95],
            [1124, 0, 126, 94],
            [1125, 282, 125, 92],
            [1125, 374, 374, 96],
            [1750, 375, 250, 87],
            [500, 376, 124, 93],
            [375, 469, 249, 187],
            [0, 470, 124, 186],
            [1125, 470, 125, 279],
            [500, 656, 124, 281],
            [1125, 1033, 124, 188],
            [502, 1127, 123, 94],
            [253, 1221, 1120, 92],
            [1625, 1221, 375, 92],
        ],
        OBJECTS=[
            classes.Interactable([5, 5], None, name="Box"),
            classes.Interactable([170, 295], None, name="Box"),
            classes.Interactable([560, 210], None, name="Box"),
            classes.Interactable([820, 5], None, name="Box"),
            classes.Interactable([845, 585], None, name="Box"),
            classes.Interactable([281, 295], None, name="Box"),
            classes.Interactable([2, 622], None, name="Box"),
            classes.Interactable(
                [390, 0],
                None,
                name="Exit",
                type="door",
                door_dest="Overworld",
                active=False,
            ),
        ],
        SPAWNPOINT=[390, 40],
    ),
    Map(
        "Manufactory",
        "map2.png",
        "nav_mesh_manufactory.txt",
        [0, 0],
        mouse_conversion,
        [2500, 2500],
        POLYGONS=[
            [468, 0, 155, 76],
            [2034, 0, 156, 310],
            [467, 233, 156, 78],
            [0, 311, 623, 156],
            [1095, 312, 468, 155],
            [1564, 312, 155, 783],
            [1095, 467, 154, 313],
            [2034, 625, 154, 156],
            [2034, 781, 466, 156],
            [311, 782, 155, 782],
            [1094, 1095, 625, 154],
            [1564, 1249, 155, 159],
            [1564, 1408, 626, 155],
            [2034, 1563, 155, 471],
            [311, 1564, 938, 155],
            [0, 2034, 466, 156],
            [781, 2034, 312, 156],
            [1407, 2034, 782, 155],
            [938, 2190, 155, 310],
        ],
        OBJECTS=[
            classes.Interactable([5, 5], None, name="Box"),
            classes.Interactable([560, 210], None, name="Box"),
            classes.Interactable([210, 605], None, name="Box"),
            classes.Interactable([830, 700], None, name="Box"),
            classes.Interactable([770, 530], None, name="Box"),
            classes.Interactable([970, 5], None, name="Box"),
            classes.Interactable([5, 980], None, name="Box"),
            classes.Interactable(
                [400, 0],
                None,
                name="Exit",
                type="door",
                door_dest="Overworld",
                active=False,
            ),
        ],
        SPAWNPOINT=[100, 100],
    ),
    Map(
        "Liberation",
        "map3.png",
        "nav_mesh3.txt",
        [0, 0],
        mouse_conversion,
        [2500, 2500],
        POLYGONS=[
            [1251, 0, 113, 219],
            [449, 219, 112, 115],
            [1251, 219, 342, 115],
            [1824, 219, 457, 113],
            [334, 334, 457, 113],
            [1022, 334, 342, 113],
            [219, 447, 228, 114],
            [1022, 447, 112, 345],
            [219, 561, 113, 688],
            [2168, 563, 332, 113],
            [2168, 676, 113, 344],
            [792, 792, 457, 113],
            [563, 1136, 686, 113],
            [1136, 1249, 113, 460],
            [2053, 1251, 228, 113],
            [2053, 1364, 113, 345],
            [219, 1480, 113, 229],
            [219, 1709, 342, 113],
            [792, 1709, 801, 113],
            [1824, 1709, 342, 113],
            [219, 1822, 113, 117],
            [792, 1822, 113, 231],
            [2053, 1822, 113, 230],
            [0, 1939, 332, 113],
            [563, 2053, 801, 113],
            [1652, 2111, 113, 112],
            [1251, 2166, 113, 115],
            [2053, 2282, 113, 218],
            [563, 2397, 113, 103],
        ],
        OBJECTS=[
            classes.Interactable([5, 5], None, name="Box"),
            classes.Interactable([560, 210], None, name="Box"),
            classes.Interactable([210, 605], None, name="Box"),
            classes.Interactable([830, 700], None, name="Box"),
            classes.Interactable([770, 530], None, name="Box"),
            classes.Interactable([970, 5], None, name="Box"),
            classes.Interactable([5, 980], None, name="Box"),
            classes.Interactable(
                [400, 0],
                None,
                name="Exit",
                type="door",
                door_dest="Overworld",
                active=False,
            ),
        ],
        SPAWNPOINT=[400, 60],
    ),
]
