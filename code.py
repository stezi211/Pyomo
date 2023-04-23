import pyomo.environ as pyo

model = pyo.AbstractModel(name = "wd")

model.I = pyo.Set()
model.L = pyo.Set()
model.C = pyo.Set()

model.Incineration_Cost = pyo.Param(model.I)
model.Incineration_Capacity = pyo.Param(model.I)

model.Landfill_Capacity = pyo.Param(model.L)

model.Wastage = pyo.Param(model.C)

model.Distances_to_I = pyo.Param(model.I, model.C | model.L)

model.ReduceWasteToDebris = pyo.Param()
model.TransportationCost = pyo.Param()

# Synolo sto opoio kinountai oi metavlhtes

def bnd_rule(model,i,j):
    return(0.0, None)

model.x = pyo.Var(model.I, model.C | model.L, bounds = bnd_rule)

# Antikeimenikh synarthsh

def obj_rule(model):
    return(sum(((model.Distances_to_I[i,j]*model.TransportationCost + model.Incineration_Cost[i])*model.x[i,j]) for i in model.I for j in model.C) +
           sum(((model.Distances_to_I[i,j]*model.TransportationCost)*model.x[i,j]) for i in model.I for j in model.L))

model.OBJ = pyo.Objective(rule = obj_rule)

# Posa skoupidia kaloume na epexergastw

def con_waste_rule(model,j):
    return(sum(model.x[i,j] for i in model.I) == model.Wastage[j])

model.con_waste = pyo.Constraint(model.C, rule = con_waste_rule)

# diathesimos xwros sta xwrafia

def con_land_rule(model,j):
    return(sum(model.x[i,j] for i in model.I) <= model.Landfill_Capacity[j])

model.con_land = pyo.Constraint(model.L, rule = con_land_rule)

# diathesimos xwros stous apotefrothres

def con_incen_rule(model,i):
    return(sum(model.x[i,j] for j in model.C) <= model.Incineration_Capacity[i])

model.con_incen = pyo.Constraint(model.I, rule = con_incen_rule)

# diaforetiko input kai output otan pernas mesa apo to apotefrvthrio

def con_incen_input_output_rule(model,i):
    return(sum(model.ReduceWasteToDebris * model.x[i,j] for j in model.C) == sum(model.x[i,k] for k in model.L))

model.con_incen_input_output = pyo.Constraint(model.I, rule = con_incen_input_output_rule)
