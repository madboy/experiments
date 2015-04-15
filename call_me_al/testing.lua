local testing = {}
local l = require("list")

local results = {}

function testing.assert_equal(expected, actual)
    if type(expected) == 'table' then
        if l.compare(expected, actual) then
            table.insert(results, ".")
            return true, ""
        else
            local f = string.format("Expected {%s} but was {%s}", l.join(expected, ","), l.join(actual, ","))
            table.insert(results, "f")
            return false, f
        end
    elseif expected == actual then
        table.insert(results, ".")
        return true, ""
    else
        local f = string.format("Expected %s but was %s", expected, actual)
        table.insert(results, "f")
        return false, f
    end
end

function testing.assert_error(func, args)
    local status, exception = pcall(func, args)
    if not status then
        table.insert(results, ".")
        return true, ""
    else
        local f = string.format("Expected error but got: %s", exception)
        table.insert(results, "f")
        return false, f
    end
end

function testing.print_results(start, stop)
    local time_spent = stop - start
    print(l.join(results))
    print("-----------------------")
    print(string.format("Ran %d tests in %.3fs", #results, time_spent))
end

function testing.run_tests(testfunctions)
    local start = os.time()
    for fname,obj in pairs(testfunctions) do
        if type(obj) == "function" then
            local success, msg = obj()
            if not success then
                print(fname, msg)
            end
        end
    end
    local stop = os.time()
    testing.print_results(start, stop)
end

return testing
