local gameIds = {
    [126884695634066] = "https://raw.githubusercontent.com/ricejay/shard/refs/heads/main/main.lua"
}

local loadScript = gameIds[game.PlaceId]
if loadScript then
    loadstring(game:HttpGetAsync(loadScript))()
end
