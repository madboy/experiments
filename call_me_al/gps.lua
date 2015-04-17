current_state = {}
local l = require('list')

function gps(goals, ops)
    -- if every goal is achieved then solved
    for _,g in ipairs(goals) do
        if achieve(g, ops) then
            print(g, "Is solved")
        end
    end
end


function achieve(goal, ops)
    -- A goal is achieved if it already holds
    -- or if there's an approriate op for it that is applicable
    if l.member(goal, current_state) then
        return true
    end
    -- some apply-op to
    -- find-all goal ops test appropriate
    print("Our goal is not yet solved need apply actions", goal)
    for _,op in pairs(ops) do
        if appropriate_op(goal, op) then
            apply_op(op, ops)
        end
    end
end

function appropriate_op(goal, op)
    -- An op is appropriate to a goal if it is in its add list
    -- member goal op-add-list op
    return l.member(goal, op.add_list)
end

function apply_op(op, ops)
    -- Print a message and update state if op is applicable
    -- when every achieve op-preconds op
    --   print("executing", op-action-op
    --   current_state = set-difference state (op-del-list op)
    --   current_state = union state (op-add-list op)
    -- when all preconditions are met we can achieve the goal?
    --
    -- when we are applying an operation we can delete what's in the del-list
    -- from the current state
    -- but we also need to add what's in the add-list to the things that are
    -- now the current state

    -- are all preconds met?
    for _,pc in ipairs(op.preconds) do
        if l.member(pc, current_state) then
            print(pc, "is already met")
        else
            print("we need to do", pc)
            achieve(pc, ops)
            for _, v in ipairs(op.del_list) do
                l.remove(current_state, v)
            end
            for _, v in ipairs(op.add_list) do
                l.add(current_state, v)
            end
        end
    end
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
                    {action='telephone-shop',
                     preconds={'know-phone-number'},
                     add_list={'in-communication-with-shop'},
                     del_list={}},
                    {action='look-up-number',
                     preconds={'have-a-phone-book'},
                     add_list={'know-phone-number'},
                     del_list={}},
                    {action='give-shop-money',
                     preconds={'have-money'},
                     add_list={'shop-has-money'},
                     del_list={'have-money'}}}

current_state = {'son-at-home', 'car-needs-battery', 'have-money', 'have-a-phone-book'}
l.print(current_state)
gps({'son-at-school'}, school_ops)
l.print(current_state)

-- expected
-- executing look-up-number
-- executing telephone-shop
-- executing tell-shop-problem
-- executing give-shop-money
-- executing shop-installs-battery
-- executing drive-son-to-school
-- solved
