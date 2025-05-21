local gameIds = {
    [126884695634066] = "GrowAGarden"
}

local loadScript = gameIds[game.PlaceId]
if loadScript then
    loadstring(game:HttpGetAsync(loadScript))()
end
