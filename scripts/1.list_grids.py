from mysg.util import combinations

# 1. Source
models = ['s']

# 2. Disk
models = combinations(models, ['-','p'])
# models = combinations(models, ['-','p','a'])

# 3. Envelope
models = combinations(models, ['-','p','u'])

# 4. Cavity
models = combinations(models, ['-','b'])

# 5. Inner Hole
models = combinations(models, ['s','h'])

# 6. Ambient medium
models = combinations(models, ['-','m'])

# 7. Dust
models = combinations(models, ['i'])
# models = combinations(models, ['i','g'])

# 8. PAH/VSG
models = combinations(models, ['-'])
# models = combinations(models, ['-','p'])

# 9. Spare
models = combinations(models, ['-'])

# 10. Spare
models = combinations(models, ['-'])

# 11. Spare
models = combinations(models, ['-'])

# 12. Spare
models = combinations(models, ['-'])

# Find models that don't make sense
remove = []
for model in models:
    if model[2] != '-' and model[5] == '-':
        remove.append(model)
    if model[3] == 'b' and model[2] == '-':      
        remove.append(model)
    if model[4] == 'h' and model[:4] == 's---':
        remove.append(model)

# Remove duplicates
remove = list(set(remove))

# Remove these models
for model in remove:
    models.remove(model)

# Sort alphanumerically
models.sort()

# Write the grids out to a file
f = open('grids.txt', 'wb')
for model in models:
    f.write("%s\n" % model)
f.close()

