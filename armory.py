from values import *
import weapons.melee as Melee
import weapons.gun as W
from weapons.area import Grenade
from weapons.area import Explosion

guns = {
    "M1911": W.Gun(
        name="M1911",
        price=135,
        clip_s=8,
        fire_r=2000,
        spread=7,
        spread_r=0.94,
        reload_r=45,
        damage=34,
        semi_auto=True,
        bullets_at_once=1,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="m1911.png",
        ammo="INF",
        view=0.0,
        handling=0.7,
    ),

    "FN57-S": W.Gun(
        name="FN57-S",
        price=1000,
        clip_s=12,
        fire_r=2000,
        spread=0.5,
        spread_r=0.9,
        reload_r=30,
        damage=45,
        bullet_speed=35,
        semi_auto=True,
        bullets_at_once=1,
        sounds=pistol_sounds_silenced,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="fn.png",
        ammo="9MM",
        view=0.02,
        handling=0.9,
    ),

    "DESERT EAGLE" : W.Gun(
        name="DESERT EAGLE",
        price=950,
        clip_s=7,
        fire_r=2000,
        spread=0.5,
        spread_r=0.955,
        spread_per_bullet = 20,
        reload_r=50,
        damage=75,
        bullet_speed=45,
        semi_auto=True,
        bullets_at_once=1,
        sounds=sniper_rifle_sounds,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="desert.png",
        ammo="50 CAL",
        view=0.022,
        handling=0.35,
        piercing=True,
        ai_fire_rate_mod = 15,
    ),

    "AR-15": W.Gun(
        name="AR-15",
        price=2900,
        clip_s=35,
        fire_r=500,
        spread=1,
        spread_r=0.93,
        bullet_speed=35,
        reload_r=60,
        damage=29,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="m16.png",
        ammo="7.62x39MM",
        piercing=True,
        view=0.032,
        handling=0.25,
        burst=True,
        burst_bullets=3,
        burst_fire_rate=2,
    ),
    "AK": W.Gun(
        name="AK47",
        price=2700,
        clip_s=30,
        fire_r=520,
        spread=3,
        spread_r=0.94,
        bullet_speed=25,
        reload_r=60,
        damage=34,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="ak.png",
        ammo="7.62x39MM",
        piercing=True,
        view=0.03,
        handling=0.35,
    ),
    "SCAR18": W.Gun(
        name="SCAR18",
        price=1700,
        clip_s=20,
        fire_r=240,
        spread=1,
        spread_r=0.945,
        bullet_speed=30,
        spread_per_bullet=2,
        reload_r=45,
        damage=45,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds2,
        ammo_cap_lvlup=1,
        image="scar.png",
        ammo="50 CAL",
        piercing=True,
        view=0.035,
        handling=0.45,
    ),
    "M134 MINIGUN": W.Gun(
        name="M134 MINIGUN",
        price=6500,
        clip_s=999,
        fire_r=2300,
        spread=2,
        spread_r=0.96,
        bullet_speed=45,
        reload_r=120,
        damage=34,
        bullets_at_once=1,
        shotgun=False,
        sounds=assault_rifle_sounds,
        ammo_cap_lvlup=1,
        image="m134.png",
        ammo="5.56x45MM NATO",
        piercing=True,
        view=0.03,
        handling=0.1,
    ),
    "RPG-7": W.Gun(
        name="RPG-7",
        price=2300,
        clip_s=1,
        fire_r=2300,
        spread=2,
        spread_r=0.96,
        bullet_speed=45,
        reload_r=75,
        damage=1000,
        bullets_at_once=1,
        shotgun=False,
        sounds=rocket_launcher_sounds,
        ammo_cap_lvlup=1,
        image="rpg.png",
        ammo="INF",
        view=0.03,
        handling=0.2,
        rocket_launcher = True,
        semi_auto = True,
        extra_bullet = False,
    ),

    "SPAS": W.Gun(
        name="SPAS-12",
        price=1300,
        clip_s=6,
        fire_r=120,
        spread=5,
        spread_per_bullet=2,
        spread_r=0.93,
        reload_r=60,
        damage=22,
        bullet_speed=15,
        bullets_at_once=8,
        shotgun=True,
        semi_auto=True,
        sounds=shotgun_sounds,
        ammo_cap_lvlup=2,
        image="spas12.png",
        ammo="12 GAUGE",
        view=0.01,
        handling=0.2,
    ),
    "P90": W.Gun(
        name="P90",
        price=900,
        clip_s=50,
        fire_r=950,
        spread=7,
        spread_r=0.94,
        reload_r=60,
        damage=21,
        bullets_at_once=1,
        shotgun=False,
        sounds=smg_sounds,
        ammo_cap_lvlup=2,
        image="p90.png",
        ammo="9MM",
        view=0.02,
        handling=0.5,
    ),
    "MP5": W.Gun(
        name="MP5",
        price=750,
        clip_s=40,
        fire_r=600,
        spread=2,
        spread_r=0.93,
        spread_per_bullet=3.4,
        reload_r=44,
        damage=24,
        bullets_at_once=1,
        shotgun=False,
        sounds=smg_sounds,
        ammo_cap_lvlup=2,
        image="mp5.png",
        ammo="45 ACP",
        view=0.02,
        handling=0.5,
        burst=True,
        burst_bullets=4,
        burst_fire_rate=2,
    ),
    "GLOCK": W.Gun(
        name="GLOCK",
        price=350,
        clip_s=20,
        fire_r=350,
        spread=3,
        spread_r=0.92,
        reload_r=30,
        damage=27,
        semi_auto=False,
        bullets_at_once=1,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="glock.png",
        ammo="45 ACP",
        view=0.017,
        handling=0.9,
        burst=True,
        burst_bullets=3,
        burst_fire_rate=3,
    ),
    "AWP": W.Gun(
        name="AWP",
        price=1500,
        clip_s=10,
        fire_r=50,
        spread=1,
        spread_r=0.965,
        spread_per_bullet=25,
        reload_r=80,
        damage=200,
        bullets_at_once=1,
        sounds=sniper_rifle_sounds,
        bullet_speed=55,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="awp.png",
        ammo="50 CAL",
        piercing=True,
        view=0.045,
        handling=0.15,
        semi_auto=True,
        ai_fire_rate_mod = 40,
    ),
    "NRG-LMG Mark1": W.Gun(
        name="NRG-LMG Mark1",
        price=6700,
        clip_s=67,
        fire_r=600,
        spread=1,
        spread_r=0.935,
        spread_per_bullet=2.2,
        reload_r=80,
        damage=75,
        bullets_at_once=1,
        sounds=nrg_sounds,
        bullet_speed=45,
        shotgun=False,
        ammo_cap_lvlup=1,
        image="nrg.png",
        ammo="Energy Cell",
        piercing=True,
        view=0.035,
        handling=0.25,
        semi_auto=False,
        energy_weapon=True,
        charge_up=True,
        charge_time=30,
    ),
}
melees = {}
grenades = {}
__weapons_map = {"gun": guns, "melee": melees, "grenade": grenades}
