--[[
-- Legendary Companions
--]]
local config = {
    -- Party buffs
    ['friendly_spawn_buff_party'] = true,
    -- Spawn buffs
    ['friendly_spawn_buff_self'] = true,
    ['hostile_spawn_buff_self'] = false,
}
local EVIL_FACTION_ID = 'Evil_NPC_64321d50-d516-b1b2-cfac-2eb773de1ff6'
local creatures = {
    --[[
    'Monstrosity_Mimic_4f694363-716d-48be-bb05-bfcf558a081f',
    'MOO_KethericHound_1d7a1689-9707-4358-bc2b-075e8520cef8',
    'Undead_Skeleton_Caster_edb2601b-7f01-44e5-84df-7513a695d4eb',
    'Dog_343975da-acc9-4803-8caf-2aed017e3ca8',
    -- 'Dragon_Red_64383f18-9830-40c2-8681-657cf36afc05',
    'Crab_001_50daafea-3ce4-4cc6-ae4e-56966a0f4e12',
    --]]
    --[[
    -- Spectators
    {
        ['template_ids'] = {
            'Spectator_Alpha-3ea81eff-2f15-4d06-aa9f-5fa99dbec632',
            'Specator_Beta_29364cf7-8a8c-47fc-b5f9-4b51b24e3845',
        },
        ['buff_party_spells'] = {
            'EC_Target_Longstrider_AOE',
        },
        ['self_status'] = {

        }
    },
    --]]
    -- Githzerai
    {
        ['summon_spell'] = '',
        ['template_ids'] = {
            LC_GITHZERAI_COMMON,
            --'b0c13825-1346-4e9e-b43a-5f54de1577a0',
            --'LC_githzerai_raider_b0c13825-1346-4e9e-b43a-5f54de1577a0',
            --'Githyanki_Male_Civilian_e1eedf2d-5b9e-480c-bdd3-6e108e4740e5',
        },
        ['buff_party_spells'] = {
            'Target_PLA_Githyanki_Rally',
        },
        ['self_status'] = {
            'WARMAGIC_GITHYANKI',
        }
    },
    --[[
    -- Hound
    {
        ['template_ids'] = {
            'MOO_KethericHound_1d7a1689-9707-4358-bc2b-075e8520cef8',
        },
        ['buff_party_spells'] = {
            'Shout_Aid',
        },
        ['self_status'] = {
            'Target_PLA_Githyanki_Rally',
        }
    },
    --]]
    --[[ Abuela
    {
        ['template_ids'] = {
            -- naked man
            --'Humans_Female_HagDouble_2ec6e2a6-2b93-4f7d-899c-bad10d93ea38',
        },
        ['buff_party_spells'] = {
            'Shout_Aid',
        },
        ['self_status'] = {

        }
    },
    --]]
}
local creature_buff_spells = {
    --'Target_Bless_3_AI',
    --'EC_Target_Enlarge_AOE',
    --'EC_Target_Haste_AOE',
    'EC_Target_Longstrider_AOE'
}
local function is_friend()
    return math.random(0, 1) == 1
end
local last_spawned_creature = ''
local last_spawned_creature_info = nil
local buffed_creatures = {}
local spawned_creature_spell_queue = {}

local function get_guid_from_tpl(tpl_id)
    return string.sub(tpl_id, -36)
end

local function set_creature_hostile(creature_tpl_id)
    Osi.SetFaction(creature_tpl_id, EVIL_FACTION_ID)
    MuffinLogger.info(string.format('Set hostile on %s', creature_tpl_id))
end

local function set_creature_level_equal_to_host(creature_tpl_id)
    local host = Osi.GetHostCharacter()
    if host then
        local level = Osi.GetLevel(host)
        if level then
            Osi.SetLevel(creature_tpl_id, tonumber(level))
        end
    end
end

local function get_random_creature_info(creature_table)
    local keyset = {}
    for k in pairs(creature_table) do
        table.insert(keyset, k)
    end
    return creature_table[keyset[math.random(#keyset)]]
end

local function handle_friendly_spawn(creature_tpl_id)
    Osi.AddPartyFollower(creature_tpl_id, Osi.GetHostCharacter())
end

local function handle_hostile_spawn(creature_tpl_id)
    set_creature_hostile(creature_tpl_id)
    -- TODO maybe they buff themselves or debuff player here
end

--[[
-- Creatures that are spawned can't cast spells immediately;
-- we have to wait for them to be on stage. We queue up a spell
-- here in anticipation of the event handler
--]]
local function add_buffs_to_creature(creature_tpl_id)
    local rnd_spell_name = creature_buff_spells[math.random(#creature_buff_spells)]
    if rnd_spell_name then
        --spawned_creature_spell_queue[rnd_spell_name] = creature_tpl_id
        Osi.UseSpell(creature_tpl_id, rnd_spell_name, creature_tpl_id)
        MuffinLogger.info(string.format('Queued spell %s with target %s', rnd_spell_name, creature_tpl_id))
    end
end

-- @param party_member_tpl string
-- @return nil
local function add_party_buffs(party_member_tpl)
    if last_spawned_creature and last_spawned_creature_info then
        if #last_spawned_creature_info['buff_party_spells'] > 0 then
            local spells = last_spawned_creature_info['buff_party_spells']
            local rnd_party_buff = spells[math.random(#spells)]
            --spawned_creature_spell_queue[rnd_party_buff] = party_member_tpl
            Osi.UseSpell(last_spawned_creature, rnd_party_buff, party_member_tpl)
            MuffinLogger.debug(string.format('Queued creature buff: %s', rnd_party_buff))
        else
            add_buffs_to_creature(party_member_tpl)
        end
    end
end

-- Remove is here to prevent stacking on multiple
-- of the same creature
local function apply_general_creature_status()
    Osi.RemoveStatus(last_spawned_creature, 'EC_AUTOMATED')
    Osi.ApplyStatus(last_spawned_creature, 'EC_AUTOMATED', -1, 1, last_spawned_creature)
end

local function apply_spawn_self_status(status_name)
    if last_spawned_creature_info and last_spawned_creature_info['self_status'] then
        local statuses = last_spawned_creature_info['self_status']
        if #statuses > 0 then
            local rnd_status = statuses[math.random(#statuses)]
            MuffinLogger.debug(string.format('Applying creature self status %s to %s', rnd_status, last_spawned_creature))
            Osi.RemoveStatus(last_spawned_creature, rnd_status)
            Osi.ApplyStatus(last_spawned_creature, rnd_status, -1, 1, last_spawned_creature)
        end
    end
end

local function handle_spawn_equipment()
    if last_spawned_creature_info then
        local items = last_spawned_creature_info['add_equipment']
        if items then
            for _, item_tpl in pairs(items) do
                -- Osi.Equip(last_spawned_creature, item_tpl)
                -- Osi.Equip(Osi.GetHostCharacter(), item_tpl)
                MuffinLogger.debug(string.format('Equipped %s with %s', last_spawned_creature, item_tpl))
            end
        end
    end
end

local function handle_creature_spawn()
    if last_spawned_creature_info then
        local creature_tpl_id = last_spawned_creature_info['spawned_guid']

        -- Creature statuses
        apply_general_creature_status()
        if last_spawned_creature_info['self_status'] then
            apply_spawn_self_status()
        end
        buffed_creatures[last_spawned_creature] = 1

        -- Handle equipment
        handle_spawn_equipment()

        -- Handle spells

        -- Handle hostility
        --[[
        if is_friend then
            handle_friendly_spawn(creature_tpl_id)
        --else
            handle_hostile_spawn(creature_tpl_id)
        --end
        ]]
        handle_friendly_spawn(creature_tpl_id)
        --handle_hostile_spawn(creature_tpl_id)

        -- Set creature level and buffs
        set_creature_level_equal_to_host(creature_tpl_id)
        -- add_buffs_to_creature(creature_tpl_id)

        -- Party buffs
        --if is_friend and config['friendly_spawn_buff_party'] then
        MuffinLogger.info('Adding buffs to party')
        local party_member_tpl = get_guid_from_tpl(Osi.GetHostCharacter())
        add_party_buffs(party_member_tpl)
        --end

        last_spawned_creature_info['handled_spawn'] = true
    end
end

local function spawn_creature()
    last_spawned_creature_info = get_random_creature_info(creatures)
    local templates = last_spawned_creature_info['template_ids']
    local summon_spell = last_spawned_creature_info['summon_spell']

    if #templates > 0 then
        local rnd_creature_tpl_id = templates[math.random(#templates)]
        local x, y, z = Osi.GetPosition(tostring(Osi.GetHostCharacter()))
        local x_num = tonumber(x)
        local is_friendly = is_friend()
        MuffinLogger.info(string.format('Spawning a %s at %s, %s, %s', rnd_creature_tpl_id, x, y, z))

        -- Give some space if this is a hostile creature
        if not is_friendly then
            x = x + 10
            y = y + 10
        end

        if x_num ~= nil then
            local created_guid = Osi.CreateAt(rnd_creature_tpl_id, x_num, y, z, 0, 1, '')
            if created_guid ~= nil then
                MuffinLogger.debug('Successful spawn')
                last_spawned_creature = tostring(created_guid)
                last_spawned_creature_info['spawned_guid'] = last_spawned_creature
                last_spawned_creature_info['handled_spawn'] = false
            else
                MuffinLogger.critical(string.format('Failed to spawn %s', rnd_creature_tpl_id))
            end
        end
    else
        if summon_spell then
            MuffinLogger.debug(string.format('Casting summoning spell: %s', summon_spell))
            local host_char = tostring(Osi.GetHostCharacter())
            Osi.UseSpell(host_char, summon_spell, host_char)
            last_spawned_creature_info['spawned_guid'] = nil
            last_spawned_creature_info['handled_spawn'] = false
        end
    end
end

local function on_item_opened(item_template_id)
    MuffinLogger.info(string.format('Opened item %s', item_template_id))
    spawn_creature()
end

local function remove_spell_from_queue(spell_name, target_guid)
    spawned_creature_spell_queue[spell_name] = nil
    MuffinLogger.debug(string.format('Removed spell %s [%s] from queue', spell_name, target_guid))
end

local function get_party_members()
    local party_members = {}
    for _, row in pairs(Osi.DB_PartyMembers:Get(nil)) do
        table.insert(party_members, row[1])
    end
    return party_members
end

local function on_went_on_stage(object_guid, is_on_stage_now)
    if is_on_stage_now then
        if last_spawned_creature then
            local already_buffed = buffed_creatures[last_spawned_creature] == object_guid
            if object_guid == last_spawned_creature and not already_buffed then
                -- TODO copy this status into EC mod
                -- TODO make this only apply to friendlies
                if last_spawned_creature_info and not last_spawned_creature_info['handled_spawn'] then
                    handle_creature_spawn()
                end
            end
        end
    end
end

local function on_casted_spell(caster, spell, spellType, spellElement, storyActionID)
    local queued_spell_target = spawned_creature_spell_queue[spell]
    local is_creature_caster = get_guid_from_tpl(caster) == last_spawned_creature
    local is_creature_spell = queued_spell_target ~= nil

    if is_creature_caster and is_creature_spell then
        MuffinLogger.debug(string.format('Casting %s on %s', spell, queued_spell_target))
        Osi.UseSpell(last_spawned_creature, spell, queued_spell_target)
        remove_spell_from_queue(spell, queued_spell_target)
        MuffinLogger.debug(string.format('Removed spell %s from queue', spell))
    end
end

local function on_template_added_to(objectTemplate, object2, inventoryHolder, addType)
    MuffinLogger.critical(string.format('Added item %s to %s', objectTemplate, inventoryHolder))
end

local function on_book_read(character, book_name)
    MuffinLogger.debug('BOOK READ!!')
    MuffinLogger.debug(book_name)
end

Ext.Osiris.RegisterListener('WentOnStage', 2, 'after', on_went_on_stage)
Ext.Osiris.RegisterListener('Opened', 1, 'after', on_item_opened)
Ext.Osiris.RegisterListener('TemplateAddedTo', 4, 'after', on_template_added_to)
Ext.Osiris.RegisterListener('OpenCustomBookUI', 2, 'after', on_book_read)
-- TODO add death handler that removes creatures and from buff table
