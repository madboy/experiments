--local state = {}
--local ops = {}
--local op = {action=nil, preconds=nil, add_list=nil, del_list=nil}
local l = require('list')

function gps(state, goals, ops)
    for _,g in ipairs(goals) do
        if achieve(state, g, ops) then
            print(g, "Is solved")
        end
    end
end


function achieve(state, goal, ops)
    -- find all appropriate ops for a goal
    for _,op in ipairs(ops) do
        appropriate_op(state, goal, op)
    end
end

function appropriate_op(goal, op)
    for _,o in ipairs(op.add_list) do
        if op == o then
            return true
        end
    end
end

function apply_op(op)
    -- when all preconditions are met we can achieve the goal?
end

local school_ops = {{action='drive-son-to-school',
                     preconds={'son-at-home', 'car-works'},
                     add_list={'son-at-school'},
                     del_list={'son-at-home'}},
                    {action='shop-installs-battery',
                     preconds={'car-need-battery', 'shop-knows-problem', 'shop-has-money'},
                     add_list={'car-works'},
                     del_list={}},
                    {action='tell-shop-problem',
                     preconds={'in-communication-with-shop'},
                     add_list={'shop-knows-problem'},
                     del_list={}},
                    {action='look-up-number',
                     preconds={'have-a-phone-book'},
                     add_list={'know-phone-number'},
                     del_list={}},
                    {action='give-shop-money',
                     preconds={'have-money'},
                     add_list={'shop-has-money'},
                     del_list={'have-money'}}}

local current_state = {'son-at-home', 'car-needs-battery', 'have-money', 'have-phone-book'}
gps(current_state, {'son-at-school'}, school_ops)
