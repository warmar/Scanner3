IDS_ONLY = True
VERSION = '1.2.7'

STATUSES = {
    -2: {'name': 'Unknown', 'color': '#FFFFFF'},
    -1: {'name': 'In-Game', 'color': '#8CB359'},
    0: {'name': 'Offline', 'color': '#5E5B58'},
    1: {'name': 'Online', 'color': '#86B5D9'},
    2: {'name': 'Busy', 'color': '#86B5D9'},
    3: {'name': 'Away', 'color': '#86B5D9'},
    4: {'name': 'Snooze', 'color': '#86B5D9'},
    5: {'name': 'Looking to Trade', 'color': '#86B5D9'},
    6: {'name': 'Looking to Play', 'color': '#86B5D9'}
}

QUALITIES = {
    0: {'name': 'Normal', 'color': '#B2B2B2'},
    1: {'name': 'Genuine', 'color': '#4D7455'},
    3: {'name': 'Vintage', 'color': '#476291'},
    5: {'name': 'Unusual', 'color': '#8650AC'},
    6: {'name': 'Unique', 'color': '#FFD700'},
    7: {'name': 'Community', 'color': '#70B04A'},
    8: {'name': 'Valve', 'color': '#A50F79'},
    9: {'name': 'Self-Made', 'color': '#70B04A'},
    11: {'name': 'Strange', 'color': '#CF6A32'},
    13: {'name': 'Haunted', 'color': '#38F3AB'},
    14: {'name': 'Collectors', 'color': '#AA0000'},
    15: {'name': 'Decorated', 'color': '#FAFAFA'}
}

SKINS = {15000: 'Night Owl Sniper Rifle', 15001: 'Woodsy Widowmaker SMG', 15002: 'Night Terror Scattergun',
         15003: 'Backwoods Boomstick Shotgun', 15004: 'King of the Jungle Minigun', 15005: 'Forest Fire Flame Thrower',
         15006: 'Woodland Warrior Rocket Launcher', 15007: 'Purple Range Sniper Rifle', 15008: 'Masked Mender Medi Gun',
         15009: 'Sudden Flurry Stickybomb Launcher', 15010: 'Wrapped Reviver Medi Gun',
         15011: 'Psychedelic Slugger Revolver', 15012: 'Carpet Bomber Stickybomb Launcher',
         15013: 'Red Rock Roscoe Pistol', 15014: 'Sand Cannon Rocket Launcher', 15015: 'Tartan Torpedo Scattergun',
         15016: 'Rustic Ruiner Shotgun', 15017: 'Barn Burner Flame Thrower', 15018: 'Homemade Heater Pistol',
         15019: 'Lumber From Down Under Sniper Rifle', 15020: 'Iron Wood Minigun', 15021: 'Country Crusher Scattergun',
         15022: 'Plaid Potshotter SMG', 15023: 'Shot in the Dark Sniper Rifle',
         15024: 'Blasted Bombardier Stickybomb Launcher', 15025: 'Reclaimed Reanimator Medi Gun',
         15026: 'Antique Annihilator Minigun', 15027: 'Old Country Revolver',
         15028: 'American Pastoral Rocket Launcher', 15029: 'Backcountry Blaster Scattergun',
         15030: 'Bovine Blazemaker Flame Thrower', 15031: 'War Room Minigun', 15032: 'Treadplate Tormenter SMG',
         15033: 'Bogtrotter Sniper Rifle', 15034: 'Earth, Sky and Fire Flame Thrower',
         15035: 'Hickory Hole-Puncher Pistol', 15036: 'Spruce Deuce Scattergun', 15037: 'Team Sprayer SMG',
         15038: 'Rooftop Wrangler Stickybomb Launcher', 15039: 'Civil Servant Medi Gun', 15040: 'Citizen Pain Minigun',
         15041: 'Local Hero Pistol', 15042: 'Mayor Revolver', 15043: 'Smalltown Bringdown Rocket Launcher',
         15044: 'Civic Duty Shotgun', 15045: 'Liquid Asset Stickybomb Launcher', 15046: 'Black Dahlia Pistol',
         15047: 'Lightning Rod Shotgun', 15048: 'Pink Elephant Stickybomb Launcher', 15049: 'Flash Fryer Flame Thrower',
         15050: 'Spark of Life Medi Gun', 15051: 'Dead Reckoner Revolver', 15052: 'Shell Shocker Rocket Launcher',
         15053: 'Current Event Scattergun', 15054: 'Turbine Torcher Flame Thrower', 15055: 'Brick House Minigun',
         15056: 'Sandstone Special Pistol', 15057: 'Aqua Marine Rocket Launcher', 15058: 'Low Profile SMG',
         15059: 'Thunderbolt Sniper Rifle', 15060: 'Macabre Web Pistol', 15061: 'Nutcracker Pistol',
         15062: 'Boneyard Revolver', 15063: 'Wildwood Revolver', 15064: 'Macabre Web Revolver',
         15065: 'Macabre Web Scattergun', 15066: 'Autumn Flame Thrower', 15067: 'Pumpkin Patch Flame Thrower',
         15068: 'Nutcracker Flame Thrower', 15069: 'Nutcracker Scattergun', 15070: 'Pumpkin Patch Sniper Rifle',
         15071: 'Boneyard Sniper Rifle', 15072: 'Wildwood Sniper Rifle', 15073: 'Nutcracker Wrench',
         15074: 'Autumn Wrench', 15075: 'Boneyard Wrench', 15076: 'Wildwood SMG', 15077: 'Autumn Grenade Launcher',
         15078: 'Wildwood Medi Gun', 15079: 'Macabre Web Grenade Launcher', 15080: 'Boneyard Knife',
         15081: 'Autumn Rocket Launcher', 15082: 'Autumn Stickybomb Launcher',
         15083: 'Pumpkin Patch Stickybomb Launcher', 15084: 'Macabre Web Stickybomb Launcher', 15085: 'Autumn Shotgun',
         15086: 'Macabre Web Minigun', 15087: 'Pumpkin Patch Minigun', 15088: 'Nutcracker Minigun',
         15089: 'Balloonicorn Flame Thrower', 15090: 'Rainbow Flame Thrower', 15091: 'Rainbow Grenade Launcher',
         15092: 'Sweet Dreams Grenade Launcher', 15094: 'Blue Mew Knife', 15095: 'Brain Candy Knife',
         15096: 'Stabbed to Hell Knife', 15097: 'Flower Power Medi Gun', 15098: 'Brain Candy Minigun',
         15099: 'Mister Cuddles Minigun', 15100: 'Blue Mew Pistol', 15101: 'Brain Candy Pistol',
         15102: 'Shot to Hell Pistol', 15103: 'Flower Power Revolver', 15104: 'Blue Mew Rocket Launcher',
         15105: 'Brain Candy Rocket Launcher', 15106: 'Blue Mew Scattergun', 15107: 'Flower Power Scattergun',
         15108: 'Shot to Hell Scattergun', 15109: 'Flower Power Shotgun', 15110: 'Blue Mew SMG',
         15111: 'Balloonicorn Sniper Rifle', 15112: 'Rainbow Sniper Rifle', 15113: 'Sweet Dreams Stickybomb Launcher',
         15114: 'Torqued to Hell Wrench', 15115: 'Coffin Nail Flame Thrower', 15116: 'Coffin Nail Grenade Launcher',
         15117: 'Top Shelf Grenade Launcher', 15118: 'Dressed to Kill Knife', 15119: 'Top Shelf Knife',
         15120: 'Coffin Nail Medi Gun', 15121: 'Dressed to Kill Medi Gun', 15122: "High Roller's Medi Gun",
         15123: 'Coffin Nail Minigun', 15124: 'Dressed to Kill Minigun', 15125: 'Top Shelf Minigun',
         15126: 'Dressed to Kill Pistol', 15127: 'Coffin Nail Revolver', 15128: 'Top Shelf Revolver',
         15129: 'Coffin Nail Rocket Launcher', 15130: "High Roller's Rocket Launcher", 15131: 'Coffin Nail Scattergun',
         15132: 'Coffin Nail Shotgun', 15133: 'Dressed to Kill Shotgun', 15134: "High Roller's SMG",
         15135: 'Coffin Nail Sniper Rifle', 15136: 'Dressed to Kill Sniper Rifle',
         15137: 'Coffin Nail Stickybomb Launcher', 15138: 'Dressed to Kill Stickybomb Launcher',
         15139: 'Dressed to Kill Wrench', 15140: 'Top Shelf Wrench', 15141: 'Warhawk Flame Thrower',
         15142: 'Warhawk Grenade Launcher', 15143: 'Blitzkrieg Knife', 15144: 'Airwolf Knife',
         15145: 'Blitzkrieg Medi Gun', 15146: 'Corsair Medi Gun', 15147: 'Butcher Bird Minigun',
         15148: 'Blitzkrieg Pistol', 15149: 'Blitzkrieg Revolver', 15150: 'Warhawk Rocket Launcher',
         15151: 'Killer Bee Scattergun', 15152: 'Red Bear Shotgun', 15153: 'Blitzkrieg SMG',
         15154: 'Airwolf Sniper Rifle', 15155: 'Blitzkrieg Stickybomb Launcher', 15156: 'Airwolf Wrench',
         15157: 'Corsair Scattergun', 15158: 'Butcher Bird Grenade Launcher'}

WEARS = {0.2: 'Factory New', 0.4: 'Minimal Wear', 0.6: 'Field-Tested', 0.8: 'Well-Worn', 1.0: 'Battle Scarred'}

SCHEMA_OVERVIEW_URL = 'http://api.steampowered.com/IEconItems_440/GetSchemaOverview/v0001/?key=%s&language=en'
SCHEMA_ITEMS_URL = 'http://api.steampowered.com/IEconItems_440/GetSchemaItems/v0001/?key={}&start={}&language=en'
PRICELIST_URL = 'http://backpack.tf/api/IGetPrices/v4/?key=%s&raw=1'
MARKET_PRICELIST_URL = 'http://backpack.tf/api/IGetMarketPrices/v1/?key=%s'

GET_OWNED_GAMES_URL = 'http://api.steampowered.com/iplayerservice/getownedgames/v1/?key={0}&include_played_free_games=1&steamid=%s'
GET_ITEMS_URL = 'http://api.steampowered.com/ieconitems_440/getplayeritems/v0001/?key={0}&steamid=%s'
GET_SUMMARIES_URL = 'http://api.steampowered.com/isteamuser/getplayersummaries/v2/?key={0}&steamids=%s'
