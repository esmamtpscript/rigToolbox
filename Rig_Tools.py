# usefull Rig Scripts

import maya.cmds as cmds
from functools import partial
import sys


__author__ = {"autor" : "LoicLemoine"}
__version__ = {"version" : "1.0"}

#with help from Sacha Duru

"""
# Notes

prio ----
remplace shape of controller

----

Ajouter display handle
change color of controller 
namespace -> mel : namespace -mergeNamespaceWithRoot -removeNamespace "spaceJunk";
rename non rename msh/controller/sub/nodes
create ctrl /match avec edge loop
rename ctrl en sub
supprimer un grp sans avoir à deparenter 
create personal ctrl (import maya.mec as mel -> mel.eval 
orient joint avec freeze
toggle axe visibility (ik)
create controller sans skin mais option create skin
match transform avec menu deroulant avec selection transform 
ik spline cmds.connectAttr() -> translate z = taille du bones divisé par(nombre d'ik spline -1) -> curve
freeze avec joint orient
script rename same name obj -> 2 loop
merge shape
axe visibility

"""



# DEF--------------------------------------------------------------

# ------------------------------- rigging tab



# 1 script create simple hierarchy

def Create_simple_hierarchy(*args):
	# select group_parent
	sel = cmds.ls(selection=True)
	group_parent = cmds.ls(selection=True,typ='transform')


	controller_type_name = cmds.optionMenuGrp(select_controller_type, query=True, value=True)
	ctrl_name = cmds.textFieldGrp(ctrl_name_text, q=1, text=1)
	# Pas oblige de declarer une variable par argument je crois
	# grpPar=group_parent
	# ctrlName=ctrl_name
	# posX=posX
	# posY=posY
	# posZ=posZ
	if cmds.ls("root_"+ctrl_name) :
		cmds.error("controller with same name already created")
	else:
		cmds.joint(p=(0,0,0), n="sk_"+ctrl_name)
		cmds.circle(c=(0,0,0), nr=(0,1,0), n=controller_type_name+ctrl_name)
		cmds.delete(ch=True)
		cmds.group(em=True, name="root_"+ctrl_name)
		cmds.group(em=True, name="cstr_"+ctrl_name)
		cmds.parent("sk_"+ctrl_name,controller_type_name+ctrl_name)
		cmds.parent(controller_type_name+ctrl_name,"cstr_"+ctrl_name)
		cmds.parent("cstr_"+ctrl_name,"root_"+ctrl_name)

	# if not group_parent :
	# 	pass
	# else :
	# 	cmds.parent("root_"+ctrl_name, group_parent)

	# is the same thing as :
	if group_parent :
		cmds.parent("root_"+ctrl_name, group_parent)

	cmds.select(sel,r=True)


# 2 create root and cstr from a controler already created

def create_root_def( *args ):
	name_root = cmds.ls( sl=True )[0]
	create_cstr = cmds.group( name_root, n= "cstr_"+name_root[2:50])
	cmds.group( create_cstr, n= "root_"+name_root[2:50] )



# 3 matchTransform with 2 selections

def match_transform_def( *args ):
	select_1_mt= cmds.ls(sl=True)[0]
	select_2_mt= cmds.ls(sl=True)[1]
	cmds.matchTransform(select_1_mt, select_2_mt)



#4 select joint from any member selection

def select_joint_def( *args ):
	select_joint= cmds.ls(sl=True)[0]
	if cmds.ls("c_"+select_joint[2:50], sl=True):
		cmds.select("sk_"+select_joint[2:50])
	elif cmds.ls("sub_"+select_joint[4:50], sl=True):
		cmds.select("sk_"+select_joint[4:50])
	elif cmds.ls("root_"+select_joint[5:50], sl=True) or cmds.ls("cstr_"+select_joint[5:50], sl=True):
		cmds.select("sk_"+select_joint[5:50])


#5 select root from any member selection

def select_root_def( *args ):
	select_root= cmds.ls(sl=True)[0]
	if cmds.ls("c_"+select_root[2:50], sl=True):
		cmds.select("root_"+select_root[2:50])
	elif cmds.ls("sk_"+select_root[3:50], sl=True):
		cmds.select("root_"+select_root[3:50])
	elif cmds.ls("cstr_"+select_root[5:50], sl=True):
		cmds.select("root_"+select_root[5:50])
	elif cmds.ls("sub_"+select_root[4:50], sl=True):
		cmds.select("root_"+select_root[4:50])


#5 select cstr from any member selection

def select_cstr_def( *args ):
	select_cstr= cmds.ls(sl=True)[0]
	if cmds.ls("c_"+select_root[2:50], sl=True):
		cmds.select("cstr_"+select_root[2:50])
	elif cmds.ls("sk_"+select_root[3:50], sl=True):
		cmds.select("cstr_"+select_root[3:50])
	elif cmds.ls("root_"+select_root[5:50], sl=True):
		cmds.select("cstr_"+select_root[5:50])
	elif cmds.ls("sub_"+select_root[4:50], sl=True):
		cmds.select("cstr_"+select_root[4:50])



# 6 script connect attribute node to different object type

def Connect_nodeAttr_to_DifferentType(node_name,att_node_name,object_type,att_obj_name):

	sel = cmds.ls(selection=True)
	# you can select the objects if you want
	# you can specifiy any attribute like visibility draw Style outColor etc
	node_name = cmds.textFieldGrp(node_name_text, q=1, text=1)
	att_node_name=cmds.textFieldGrp(att_node_name_text, q=1, text=1)
	att_obj_name=cmds.textFieldGrp(att_obj_name_text, q=1, text=1)
	object_type = cmds.optionMenuGrp(select_object_type, query=True, value=True)
	#not necessary

	#y=type
	#z=node_name
	#w=att_node_name
	#k=att_obj_name

	if sel:
		for x in cmds.ls(selection=True, sl=True):
			cmds.connectAttr(node_name+"."+att_node_name, x + "."+att_obj_name, f=True)
	else :
		for x in cmds.ls( type=object_type, ap=True ):
			cmds.connectAttr( node_name + "."+att_node_name, x + "."+att_obj_name, f=True )

	cmds.select(sel,r=True)

# 7 script copy shape to


def Copy_shape_to(*args):

	# you have to select child curves shapes
	ctrl_Sname = cmds.textFieldGrp(ctrl_ShapeName_text, q=1, text=1)

	sel1=cmds.ls(selection=True)
	sel2=cmds.duplicate(sel1)
	cmds.matchTransform(sel2,ctrl_Sname)
	#freeze transform to place correctly the shape
	for cleaner in sel2:
		cmds.delete(cleaner, constructionHistory=True)
		cmds.makeIdentity(cleaner, apply=True, t=1, r=1, s=1, n=0)

	sel3=cmds.listRelatives(sel2, shapes=True)
	# shapes selectioned
	#sel4=cmds.listRelatives(ctrl_name, shapes=True)+sel3 useless
	cmds.parent(sel3, ctrl_Sname, add=True, shape=True)
	cmds.delete(sel2) #delete the old duplicate shapes



#8 script copy shape selected

def Copy_shape_selected():
	# your controllers shouldn't have any transform values
	#you have to select first parent curve then child curves shapes
	
	sel1=cmds.ls(os=True)
	sel2=cmds.duplicate(sel1[1:])
	cmds.matchTransform(sel2,sel1[0])
	#freeze transform to place correctly the shape
	for cleaner in sel2:
		cmds.delete(cleaner, constructionHistory=True)
		cmds.makeIdentity(cleaner, apply=True, t=1, r=1, s=1, n=0)

	sel3=cmds.listRelatives(sel2, shapes=True)
	# shapes selectioned
	#sel4=cmds.listRelatives(ctrl_name, shapes=True)+sel3 useless
	cmds.parent(sel3, sel1[0], add=True, shape=True)
	cmds.delete(sel2) #delete the old duplicate shapes



#9 script create simple rig scene

def Create_simple_Rig_Scene(*args):
	#select your mesh or your grp mesh to create the c body

	scene_Name = cmds.textFieldGrp(rigScene_Name_text, q=1, text=1)

	sel1=cmds.ls(selection=True)
	#parent mesh selection into MESHS group
	cmds.group(em=True, name="MESHS")
	if sel1:
		cmds.parent(sel1,"MESHS", r=True)

	#create base hierarchy
	grp_scene=cmds.group(em=True, name=scene_Name)
	cmds.group(em=True, name="RIG")
	cmds.group(em=True, name="OTHER")
	cmds.group(em=True, name="DEFORMERS")
	cmds.group(em=True, name="LOCATORS")
	cmds.group(em=True, name="IK")
	cmds.group(em=True, name="CTRLS")

	#parent base hierarchy
	cmds.parent("RIG",grp_scene)
	cmds.parent("MESHS",grp_scene)
	cmds.parent("OTHER",grp_scene)
	cmds.parent("DEFORMERS","RIG")
	cmds.parent("LOCATORS","RIG")
	cmds.parent("IK","RIG")
	cmds.parent("CTRLS","RIG")

	#create rig ctrls groups
	cmds.group(em=True, name="rig_main_ctrls")
	cmds.group(em=True, name="rig_final")
	cmds.group(em=True, name="rig_other_ctrls")

	#parent rig groups
	cmds.parent("rig_main_ctrls","CTRLS")
	cmds.parent("rig_other_ctrls","CTRLS")
	cmds.parent("rig_final","CTRLS")


	def Create_WORLD(ctrl_rig_1):
		# create a simple group for your WALK WORLD rig etc

		cmds.circle(c=(0,0,0),nr=(0,1,0), n="c_"+ctrl_rig_1, r=4)
		cmds.delete(ch=True)
		cmds.group(em=True, name="root_"+ctrl_rig_1)
		cmds.group(em=True, name="cstr_"+ctrl_rig_1)
		cmds.parent("c_"+ctrl_rig_1,"cstr_"+ctrl_rig_1)
		cmds.parent("cstr_"+ctrl_rig_1,"root_"+ctrl_rig_1)

	Create_WORLD("WORLD")

	def Create_WALK(ctrl_rig_2):
		# create a simple group for your WALK WORLD rig etc

		cmds.circle(c=(0,0,0),nr=(0,1,0), n="c_"+ctrl_rig_2, r=2)
		cmds.delete(ch=True)
		cmds.group(em=True, name="root_"+ctrl_rig_2)
		cmds.group(em=True, name="cstr_"+ctrl_rig_2)
		cmds.parent("c_"+ctrl_rig_2,"cstr_"+ctrl_rig_2)
		cmds.parent("cstr_"+ctrl_rig_2,"root_"+ctrl_rig_2)


	Create_WALK("WALK")

	#parent main ctrls
	cmds.parent("root_WALK","c_WORLD")
	cmds.parent("root_WORLD","rig_main_ctrls")

	'''
	#scaling WALK and WORLD
	cmds.scale(10,10,10, "root_WORLD")
	cmds.scale(0.75,0.75,0.75, "root_WALK")
	'''

	#create and parent target_main_ctrls
	cmds.group(em=True, name="target_main_ctrls")
	cmds.parent("target_main_ctrls","c_WALK")


	def Create_simple_joint_hierarchy(ctrl_name):
		# remplir les intends de la fonciton a la fin
		# select group_parent

		cmds.joint(p=(0,0,0), n="sk_"+ctrl_name)
		cmds.circle(c=(0,0,0), nr=(0,1,0), n="c_"+ctrl_name)
		cmds.delete(ch=True)
		cmds.group(em=True, name="root_"+ctrl_name)
		cmds.group(em=True, name="cstr_"+ctrl_name)
		cmds.parent("sk_"+ctrl_name,"c_"+ctrl_name)
		cmds.parent("c_"+ctrl_name,"cstr_"+ctrl_name)
		cmds.parent("cstr_"+ctrl_name,"root_"+ctrl_name)
		
	Create_simple_joint_hierarchy("body")
	
	if sel1:
		cmds.matchTransform("root_body", sel1)

	#create hook main ctrls
	def Create_hook(hook_parent,child,child_parent):
		#precise None if there isn t any child parent
		hook=cmds.group(em=True,name="hook_"+hook_parent) #create group hook
		cmds.parentConstraint(hook_parent, hook, mo=False) # parent and scale constraint
		cmds.scaleConstraint(hook_parent, hook, mo=False)

		#we can add child parent
		if child_parent:
			cmds.parent(hook,child_parent)

		if child:
			cmds.parent(child,hook) #parent child to hook

	Create_hook("target_main_ctrls","root_body","CTRLS")
	Create_hook("c_body",None,"rig_final")
	Create_hook("c_body",None,"rig_other_ctrls")

	#create rig mode and connect
	cmds.addAttr(grp_scene,ln="Rig_Mode", at="enum", en="RIGGING:ANIMATION:")
	cmds.setAttr(grp_scene+".Rig_Mode", keyable=True)
	facAttr_Rig_mode=cmds.shadingNode("multDoubleLinear",au=True, n="facAttr_"+grp_scene+"_Rig_Mode")
	cmds.connectAttr(grp_scene+".Rig_Mode",facAttr_Rig_mode+".input1", f=True) #terminal of the rig mode and usefull to connect the cond at the end
	cmds.setAttr(facAttr_Rig_mode+".input2",1,l=True)

	#create different options and facAttr
	list_options=("Unlock_Meshs","Hide_Ctrls","Show_sk","Show_Locators","Show_IK","Show_Extra_Ctrls","Show_Deformers","Show_Bones_IK")
	for options in list_options:
		cmds.addAttr(grp_scene, ln=options, at="bool")
		cmds.setAttr(grp_scene+"."+options, channelBox=True)
		cmds.shadingNode("multDoubleLinear",au=True, n="facAttr_"+grp_scene+"_"+options) #create facAttr
		cmds.setAttr("facAttr_"+grp_scene+"_"+options+".input2",1,l=True) #lock and set input 2
		cmds.connectAttr(grp_scene+"."+options,"facAttr_"+grp_scene+"_"+options+".input1", f=True) #connect facAttr input1
		cmds.shadingNode("condition",au=True,n="cond_"+grp_scene+"_"+options) #create condition Node
		cmds.connectAttr(facAttr_Rig_mode+".output","cond_"+grp_scene+"_"+options+".firstTerm", f=True)

	#connect facAttr to cond in a simple way
	list_simple_condition=("Unlock_Meshs","Show_Locators","Show_IK","Show_Extra_Ctrls","Show_Deformers")
	for connect_cond in list_simple_condition:
		cmds.setAttr("cond_"+grp_scene+"_"+connect_cond+'.colorIfTrueR',1)
		cmds.connectAttr("facAttr_"+grp_scene+"_"+connect_cond+".output","cond_"+grp_scene+"_"+connect_cond+'.colorIfFalseR', f=True)

	#connect conditions to group visibility 
	cmds.connectAttr("cond_"+grp_scene+"_Show_Locators.outColorR","LOCATORS.visibility",f=True)
	cmds.connectAttr("cond_"+grp_scene+"_Show_IK.outColorR","IK.visibility",f=True)
	cmds.connectAttr("cond_"+grp_scene+"_Show_Deformers.outColorR","DEFORMERS.visibility",f=True)

	#connections hide ctrls
	rev_Hide_ctrl=cmds.shadingNode("reverse",au=True,n="reverse_Hide_Ctrls")
	cmds.connectAttr("facAttr_"+grp_scene+"_Hide_Ctrls.output",rev_Hide_ctrl+".inputX", f=True)
	cmds.connectAttr(rev_Hide_ctrl+".outputX","cond_"+grp_scene+"_Hide_Ctrls.colorIfFalseR", f=True)
	cmds.setAttr("cond_"+grp_scene+"_Hide_Ctrls.colorIfTrueR",1)


	#set driven key connections
	#unlock mesh
	cmds.setAttr(grp_scene+".Rig_Mode",1) # set rig mode value to animation settings
	cmds.setAttr("MESHS.overrideEnabled", 1)
	cmds.setAttr(grp_scene+".Unlock_Meshs",0)
	cmds.setDrivenKeyframe ("MESHS.overrideEnabled",currentDriver="cond_"+grp_scene+"_Unlock_Meshs.outColorR") #set driven key when it is off

	cmds.setAttr(grp_scene+".Unlock_Meshs",1)
	cmds.setAttr("MESHS.overrideEnabled", 0)
	cmds.setDrivenKeyframe ("MESHS.overrideEnabled",currentDriver="cond_"+grp_scene+"_Unlock_Meshs.outColorR") #set driven key when it is on
	cmds.keyframe("MESHS_overrideEnabled",index=(1,1), absolute=True,valueChange=0) #value change it doesn t work

	cmds.setAttr("MESHS.overrideDisplayType", 2)
	cmds.setAttr(grp_scene+".Unlock_Meshs",0)
	cmds.setDrivenKeyframe ("MESHS.overrideDisplayType",currentDriver="cond_"+grp_scene+"_Unlock_Meshs.outColorR") #set driven key when it is off

	cmds.setAttr("MESHS.overrideDisplayType", 0)
	cmds.setAttr(grp_scene+".Unlock_Meshs",1)
	cmds.setDrivenKeyframe ("MESHS.overrideDisplayType",currentDriver="cond_"+grp_scene+"_Unlock_Meshs.outColorR") #set driven key when it is off
	cmds.keyframe("MESHS_overrideDisplayType",index=(1,1), absolute=True,valueChange=0) #value change it doesn t work
	# return to default value
	cmds.setAttr(grp_scene+".Unlock_Meshs",0)

	#show sk
	cmds.setAttr("cond_"+grp_scene+"_Show_sk.colorIfFalseR", 2)
	cmds.setAttr(grp_scene+".Show_sk",0)
	cmds.setDrivenKeyframe ("cond_"+grp_scene+"_Show_sk.colorIfFalseR",currentDriver="facAttr_"+grp_scene+"_Show_sk.output") #set driven key when it is off

	cmds.setAttr("cond_"+grp_scene+"_Show_sk.colorIfFalseR", 0)
	cmds.setAttr(grp_scene+".Show_sk",1)
	cmds.setDrivenKeyframe ("cond_"+grp_scene+"_Show_sk.colorIfFalseR",currentDriver="facAttr_"+grp_scene+"_Show_sk.output") #set driven key when it is off
	cmds.keyframe("cond_"+grp_scene+"_Show_sk.colorIfFalseR",index=(1,1), absolute=True,valueChange=0) #value change it doesn t work
	# return to default value
	cmds.setAttr(grp_scene+".Show_sk",0)

	#show bones ik
	cmds.setAttr("cond_"+grp_scene+"_Show_Bones_IK.colorIfFalseR", 2)
	cmds.setAttr(grp_scene+".Show_Bones_IK",0)
	cmds.setDrivenKeyframe ("cond_"+grp_scene+"_Show_Bones_IK.colorIfFalseR",currentDriver="facAttr_"+grp_scene+"_Show_Bones_IK.output") #set driven key when it is off

	cmds.setAttr("cond_"+grp_scene+"_Show_Bones_IK.colorIfFalseR", 0)
	cmds.setAttr(grp_scene+".Show_Bones_IK",1)
	cmds.setDrivenKeyframe ("cond_"+grp_scene+"_Show_Bones_IK.colorIfFalseR",currentDriver="facAttr_"+grp_scene+"_Show_Bones_IK.output") #set driven key when it is off
	cmds.keyframe("cond_"+grp_scene+"_Show_Bones_IK.colorIfFalseR",index=(1,1), absolute=True,valueChange=0) #value change it doesn t work
	# return to default value
	cmds.setAttr(grp_scene+".Show_Bones_IK",0)


	#lock transform and scale
	lock_group_list=(grp_scene,"RIG","MESHS","OTHER","CTRLS","LOCATORS","IK","LOCATORS","DEFORMERS")
	for group_lock in lock_group_list:
		cmds.setAttr(group_lock+".tx",lock=True)
		cmds.setAttr(group_lock+".ty",lock=True)
		cmds.setAttr(group_lock+".tz",lock=True)
		cmds.setAttr(group_lock+".rx",lock=True)
		cmds.setAttr(group_lock+".ry",lock=True)
		cmds.setAttr(group_lock+".rz",lock=True)
		cmds.setAttr(group_lock+".sx",lock=True)
		cmds.setAttr(group_lock+".sy",lock=True)
		cmds.setAttr(group_lock+".sz",lock=True)



#10 script create hook

def Create_hook(child_parent=None):
	#select first the parent then the child
	selection_hook=cmds.ls(os=True)
	hook=cmds.group(em=True,name="hook_"+selection_hook[0]) #create group hook
	cmds.parentConstraint(selection_hook[0], hook, mo=False) # parent and scale constraint
	cmds.scaleConstraint(selection_hook[0], hook, mo=False)

	#we can add child parent
	if child_parent:
		cmds.parent(hook,child_parent)

	cmds.parent(selection_hook[1],hook) #parent child to hook



#11 script instanced shape selected

def instanced_shape_selected():
	#you have to select first parent ctrl then child shapes
	
	sel1=cmds.ls(os=True)
	sel2=sel1[1:]
	

	sel3=cmds.listRelatives(sel2, shapes=True)
	# shapes selectioned
	#sel4=cmds.listRelatives(ctrl_name, shapes=True)+sel3 useless
	cmds.parent(sel3, sel1[0], add=True, shape=True)


# 12 Transform Scripts

def resetRotate_def(*args):
	cmds.makeIdentity( rotate=True)
	
def resetTranslate_def(*args):
	cmds.makeIdentity( translate=True)
	
def resetScale_def(*args):
	cmds.makeIdentity( scale=True)

def resetTransform_def(*args):
	resetRotate_def()
	resetTranslate_def()
	resetScale_def()

# ------------------------------- rigging tab

# controllers color --------------------
def colorize_shapes( sel=[], index=0, *args ):
	if type( sel ) is not list: sel = [sel]
	if not sel: sel = cmds.ls( sl=True, ap=True )
	if sel:
		to_color = []
		for obj in sel:
			if cmds.objectType( obj ) == "transform":
				to_color = to_color + cmds.listRelatives( obj, s=True, path=True )
			else:
				to_color.append( obj )
		for shape in to_color:
			cmds.setAttr( shape+"."+"overrideEnabled", True )
			cmds.setAttr( shape+"."+"overrideColor", index )		
	""" _controller color by Aymeric Gesse_"""

# controllers color --------------------

def help (*args):
	diUi["window"]["help"] = cmds.window(title="RigTools Help", w = 350, h = 350, minimizeButton=False, maximizeButton=False)
	diUi["lays"]["help"] = cmds.frameLayout(l="help", marginHeight=10, marginWidth=10)
	cmds.text("""- For the script 'create simple hierarchy' you can select the parent of the future controller.

	- To create controller with the name you want, you have to precise his name in the text field 'ctrl_name'. Precise if it is a sub_ or a c_. Then press ENTER.
	
	- To hook, select first the parent then the child and then press the button.
	
	- The goal of 'Select joint or root or cstr' is to select faster these items to skin, move of constraint groups.
	
	-  For the copy Shapes selected, your controllers shouldn't have any transform values you have to select first parent curve then child curves shapes.
	
	- For Copy_shape_to, it is the same thing but you have to enter parent ctrl Name and the select child curves shapes.

	- The script Create_simple_Rig_Scene will create automatically a Rig hierarchy with animation and rig mode. You have to precise your rig scene name in the text field. You can select your mesh or your grp mesh to create the c_body.

	- For the script Connect_nodeAttr_to_DifferentType, you have to precise the main node_name, his attribute, the object type you want to connect to, and then their attributes. You can select the objects if you want. You can specifiy any attribute like visibility draw Style outColor etc
	""", align="left", ww=True)
	cmds.showWindow(diUi["window"]["help"])
# DEF--------------------------------------------------------------

#MAIN WINDOW ------------------------------------------------------
# window settings -------------

diUi = {}
diUi["lays"] = {}
diUi["ctrls"] = {}
diUi["window"] = {}

#if cmds.window(diUi["window"], exists=True):
#	 cmds.deleteUI(diUi["window"])	
window = diUi["window"]["main"]= cmds.window(title="LoicRigTools", iconName="LoicRigTools", width=600, sizeable=False, minimizeButton=False, maximizeButton=False)#, height=800
diUi["lays"]["root"] = cmds.frameLayout(l="tool")
diUi["lays"]["paneH1"] = cmds.paneLayout( configuration="horizontal2", p=diUi["lays"]["root"], separatorThickness=1)
diUi["lays"]["paneV1"] = cmds.paneLayout( configuration="vertical2", p=diUi["lays"]["paneH1"], separatorThickness=1)
diUi["lays"]["tabs"]= cmds.tabLayout( innerMarginWidth=5, innerMarginHeight=5, p=diUi["lays"]["paneV1"])
diUi["lays"]["ctrl"] = cmds.columnLayout( adjustableColumn=True, p=diUi["lays"]["tabs"])
diUi["lays"]["hierarchy"] = cmds.columnLayout( adjustableColumn=True, p=diUi["lays"]["tabs"])
diUi["lays"]["Nodes"] = cmds.columnLayout( adjustableColumn=True, p=diUi["lays"]["tabs"])
cmds.tabLayout(diUi["lays"]["tabs"], edit=True, tabLabel=( (diUi["lays"]["ctrl"], "CtrlFunctions"), ( diUi["lays"]["hierarchy"], "RigScene"), (diUi["lays"]["Nodes"], "ConnectNodes")))
diUi["lays"]["transform"] = cmds.columnLayout(adjustableColumn=True, p=diUi["lays"]["paneV1"])

# c/o color -----------------------------
diUi["lays"]["cc"] = cmds.frameLayout(l="controller color",p=diUi["lays"]["paneH1"])

cmds.setParent(diUi["lays"]["cc"])
diUi["lays"]["grid"] = cmds.gridLayout(p=diUi["lays"]["cc"], numberOfRows=2, numberOfColumns=16)


# c/o color -----------------------------
diUi["lays"]["name"] = cmds.frameLayout(p=diUi["window"]["main"], l="Rig Tools by Loic Lemoine")
#-------------------


# window settings -----------


# Crl Main functions tab ----------

cmds.setParent (diUi["lays"]["ctrl"])

#cmds.button ( label="create simple hierarchy", enableBackground=True, command=Create_simple_hierarchy, backgroundColor=[0.0 , 0.8, 0.6] )

			#Menu item - c_ or sub_-----------
select_controller_type = cmds.optionMenuGrp("controller")
cmds.menuItem( label="c_" )
cmds.menuItem( label="sub_") 
			#Menu item - c_ or sub_-----------

			#Name of controller --------
ctrl_name_text = cmds.textFieldGrp( "controller_name", text="controller_name", changeCommand= Create_simple_hierarchy, enableBackground=False, adjustableColumn=1)
			#Name of controller --------

cmds.button ( label = "hook", enableBackground=True, backgroundColor=[0.0, 0.8, 1], command = Create_hook)

cmds.button ( label = "select joint", enableBackground= True, backgroundColor= [ 0.0, 0.8, 0.0 ], command= select_joint_def)

cmds.button ( label = "select root", enableBackground=True, backgroundColor= [ 0.0, 0.8, 0.0], command= select_root_def)

cmds.button ( label = "select cstr", enableBackground=True, backgroundColor= [ 0.0, 0.8, 0.0], command= select_cstr_def)

cmds.button ( label = "create root and cstr", enableBackground=True, command = create_root_def, backgroundColor=[0.0 , 0.8, 0.6])

cmds.button ( label = "Copy shape selected", enableBackground=True, command = Copy_shape_selected, backgroundColor=[0.18, 0.18, 0.18])

ctrl_ShapeName_text = cmds.textFieldGrp( "controller_Copy_Shape_Name", text="controller_Copy_Shape_Name", changeCommand= Copy_shape_to, enableBackground=False, adjustableColumn=1)
"""cmds.button ( label = "copy shapes", enableBackground=True, command= copy_shapes, backgroundColor=[0.18, 0.18, 0.18])"""

# cmds.button ( label = "merge shapes", enableBackground = True, command = merge_shapes_def, backgroundColor=[0.18, 0.18, 0.18])

	
#outliner color
#cmds.setParent (diUi["lays"]["oc"])
#cmds.button ( label = "1", enableBackground=True, backgroundColor= [0.0,0.8,0.8], command=partial.partial( khrOc.cyan, 20 ) )

# Crl Main functions tab ------



# Rig Scene tab ------


cmds.setParent (diUi["lays"]["hierarchy"])
rigScene_Name_text = cmds.textFieldGrp( "RigScene_Name", text="RigScene_Name", changeCommand= Create_simple_Rig_Scene, enableBackground=False, adjustableColumn=1)


# Rig Scene tab ------


# Connect tab ------

cmds.setParent (diUi["lays"]["Nodes"])

node_name_text = cmds.textFieldGrp( "node_name", text="Node_Name", changeCommand= Connect_nodeAttr_to_DifferentType, enableBackground=False, adjustableColumn=1)
att_node_name_text = cmds.textFieldGrp( "att_node_name_text", text="att_node_name_text", changeCommand= Connect_nodeAttr_to_DifferentType, enableBackground=False, adjustableColumn=1)
att_obj_name_text = cmds.textFieldGrp( "att_obj_name_text", text="att_obj_name_text", changeCommand= Connect_nodeAttr_to_DifferentType, enableBackground=False, adjustableColumn=1)

	#Menu item - joint or circle or locator-----------
select_object_type = cmds.optionMenuGrp("object")
cmds.menuItem( label="joint" )
cmds.menuItem( label="circle") 
cmds.menuItem( label="locator") 
	#Menu item - c_ or sub_-----------

# Connect tab ------


# transforms ---------------
cmds.setParent(diUi["lays"]["transform"])
cmds.button ( label = "match transformation", enableBackground=True, backgroundColor= [0.18,0.18,0.18], command=match_transform_def )

cmds.button ( label = "reset rotate", enableBackground=True, backgroundColor=[0.18, 0.18, 0.18], command= resetRotate_def, height=20, width= 30)

cmds.button ( label = "reset translate", enableBackground=True, backgroundColor=[0.18, 0.18, 0.18], command= resetTranslate_def, height=20, width= 30)

cmds.button ( label = "reset scale", enableBackground=True, backgroundColor=[0.18, 0.18, 0.18], command= resetScale_def, height=20, width= 30)

cmds.button ( label = "reset all tansformations", enableBackground=True, backgroundColor=[0.18, 0.18, 0.18], command=resetTransform_def)

# transforms ---------------

#controller colors ----------------

cmds.setParent(diUi["lays"]["grid"])
for x in range (0, 32):
	if x > 0:
			butt = cmds.button( l=str(x), ebg=False, bgc=cmds.colorIndex( x, q=True ) )
	else:
		butt = cmds.button( l='/' )
	
	cmds.button(butt, e=True, w=20, c=partial( colorize_shapes, [], x ) )
#controller colors ----------------
cmds.setParent(diUi["lays"]["name"])
cmds.button(label = "Help ?", command = help , w=30, h=20)

cmds.showWindow (diUi["window"]["main"])
#MAIN WINDOW -------------------------------------------------------
#UI with help from Sacha Duru