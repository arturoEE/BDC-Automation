function primeNumbers = returnPrime(maxVal)

primeNumbers = 1:maxVal;


for k = 1:maxVal
    for l = 2:floor(sqrt(k))
        if(mod(k, l) == 0)
            primeNumbers(k) = 0;
            break;
        end
    end
end

primeNumbers = find(primeNumbers ~= 0);