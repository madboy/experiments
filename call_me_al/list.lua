local list = {}

function list.sum(l)
    -- Sum will only work for lists and not dicts
    local s = 0
    for _,v in ipairs(l) do
        s = s + v
    end
    return s
end

function list.print(l)
    for _, v in ipairs(l) do
        print(v)
    end
end

function list.join(l, separator)
    local out = ""
    local s = separator or ""
    for i,v in ipairs(l) do
        out = out .. v
        if i < #l then
            out = out .. s
        end
    end
    return out
end

function list.reduce(l, f)
    local reduce = table.remove(l, 1)
    for _,v in ipairs(l) do
        reduce = f(reduce, v)
    end
    return reduce
end

function list.member(el, l)
    -- determine if el is in list
    for _,v in ipairs(l) do
        if el == v then
            return true
        end
    end
    return false
end

function list.find_all(el, l)
    -- find all instances of el in a list
    -- and return them in their own list
    local result = {}
    for _,v in ipairs(l) do
        if el == v then
            table.insert(result, v)
        end
    end
    return result
end

function list.compare(l1, l2)
    -- compare two lists element by element
    -- to determine equality
    for i,v in ipairs(l1) do
        if not (v == l2[i]) then
            return false
        end
    end
    return true
end

function list.add(l, el)
    -- add element if it's not in list
    if not list.member(el, l) then
        table.insert(l, el)
    end
end

function list.remove(l, el)
    -- remove matching element from list
    local lc = l
    for i,v in ipairs(lc) do
        if v == el then
            table.remove(l, i)
        end
    end
end
return list
