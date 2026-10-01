-- Dumps the renewal client's item list and look tables as JSON lines (run by client_data.py in a 32-bit
-- Lua 5.1 container: the kRO files are 32-bit Lua 5.1 bytecode). Strings stay in the client's cp949 bytes.
--   /c = client System folder, /d = datainfo tables extracted from data.grf, /out = output folder

local function esc(s)
  s = tostring(s)
  return (s:gsub('[%c"\\]', function(c) return string.format("\\u%04x", c:byte()) end))
end
local function enc(v)
  local t = type(v)
  if t == "table" then
    local parts, n = {}, #v
    if n > 0 then
      for i = 1, n do parts[#parts + 1] = enc(v[i]) end
      return "[" .. table.concat(parts, ",") .. "]"
    end
    for k, x in pairs(v) do parts[#parts + 1] = '"' .. esc(k) .. '":' .. enc(x) end
    return "{" .. table.concat(parts, ",") .. "}"
  elseif t == "number" then return tostring(v)
  elseif t == "boolean" then return v and "true" or "false"
  end
  return '"' .. esc(v) .. '"'
end
local function load(path, env)
  local f = loadfile(path)
  if not f then return nil end
  setfenv(f, env); local ok, err = pcall(f)
  if not ok then io.stderr:write(path .. ": " .. tostring(err) .. "\n") end
  return env
end

-- items: kRO list, English overlay (non-empty names win), our custom tickets: same order as itemInfo_true.lub
local all = {}
for _, p in ipairs({ { "/c/itemInfo_original.lub", "tbl" }, { "/c/LuaFiles514/itemInfo.lua", "tbl" }, { "/c/itemInfo_C.lua", "tbl_custom" } }) do
  local env = load(p[1], {})
  local t = env and env[p[2]]
  if t then
    for id, v in pairs(t) do
      if type(v) == "table" and (p[2] ~= "tbl" or all[id] == nil or (v.identifiedDisplayName or "") ~= "") then all[id] = v end
    end
  end
end
local out = io.open("/out/items.jsonl", "w")
for id, v in pairs(all) do out:write('{"id":', id, ',"v":', enc(v), "}\n") end
out:close()

-- look tables: headgear (view -> sprite), garments (view -> sprite), weapons (view -> sprite)
local env = {}
for _, f in ipairs({ "accessoryid.lub", "accname.lub", "spriterobeid.lub", "spriterobename.lub", "weapontable.lub" }) do
  load("/d/data.grf_" .. f, env)
end
local looks = { acc = {}, robe = {}, weapon = {} }
if env.ACCESSORY_IDs and env.AccNameTable then
  for _, id in pairs(env.ACCESSORY_IDs) do looks.acc[tostring(id)] = env.AccNameTable[id] or "" end
end
if env.SPRITE_ROBE_IDs and env.RobeNameTable then
  for _, id in pairs(env.SPRITE_ROBE_IDs) do looks.robe[tostring(id)] = env.RobeNameTable[id] or "" end
end
if env.Weapon_IDs and env.WeaponNameTable then
  for _, id in pairs(env.Weapon_IDs) do looks.weapon[tostring(id)] = env.WeaponNameTable[id] or "" end
end
local o = io.open("/out/looks.json", "w"); o:write(enc(looks)); o:close()
