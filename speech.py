# -*- coding: utf-8 -*-
### CLOTHING SPEECH OUTPUT

'''
# pseudocode
if (detection unsuccsessful):
    say = "Cannot detect item. Please try again."
else:
    follow the guidelines below
'''
####################################
############## INPUTS ############## (for testing purposes)
####################################
# NOTE: need a better way of determining color cutoffs/dominant colors

# colors
# list with the colors

#color = ["orange"]
#color = ["red", "orange"]
#color = ["red", "orange", "blue", "brown"]
color = ["red", "orange", "blue"]

# type 
# list with 0 index = class label(1-3), index 1 = type name

clothtype = [2, "leggings"]
#clothtype = [1, "sweater"]


# attributes
# dictionary mapping the attribute name to the class label(1-5)

#attr_list = {"chunky knit" : 2,"velvet" : 2 }
#attr_list = {"abstract print" : 1,"distressed" : 2,"curved hem" : 4 }
attr_list = {"chevron" : 1,"chunky knit" : 2,"high-low" : 3,"open-shoulder" : 4,"boho" : 5 }

####################################
############ FUNCTIONS #############
####################################

# COLORS 
# constructing the color syntax for colors 1 - 3 (could add more if we wanted)
colors_text = ""
def colors(colors):
    global colors_text
    colors_text = str(colors[0])
    # if one color, say as is
    if (len(colors) == 1):
        return colors_text
    # if 2 colors, add "and" in between    
    elif (len(colors) == 2):
        colors_text += " and "
        colors_text += str(colors[1])
    # if 3 colors, add commas and "and"
    elif (len(colors) == 3):
        colors_text += ", "
        colors_text += str(colors[1])
        colors_text += ", and "
        colors_text += str(colors[2])
   # if more than 3 colors, say multicolor
    else:
        colors_text = "multicolor"
        
    return colors_text

# A or AN
# determining which article to use before a color
# if a color starts with a vowel, use 'an', otherwise use 'a'
def a_an(word):
    # declaring list of vowels
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowel_text = ""
    # checking the first letter of the word
    if word[0] in vowels:
        vowel_text = " an "
    else:
        vowel_text = " a "
        
    return vowel_text

# ATTRIBUTES
# getting the attributes for constructing the sentences
texture = "" # class 1
fabric = "" # class 2
shape = "" # class 3
part_detail = "" # class 4
style = "" # class 5 
               
def attr(): 
    global texture 
    global fabric
    global shape
    global part_detail
    global style
    
    for i in attr_list.keys():
        if attr_list[i] == 1:
            texture += " " + i
        elif attr_list[i] == 2:
            fabric += " " + i
        elif attr_list[i] == 3:
            shape += " " + i
        elif attr_list[i] == 4:
            part_detail += " " + i
        elif attr_list[i] == 5:
            style += " " + i

# TEXTURE
# add 'print' to texture attribute if not already present
# e.g. 'elephant' -> 'elephant print'        
print_text = ""               
def print_or_not():
    global print_text
    # don't say anything if there is no texture attribute
    if len(texture) == 0:
        print_text = ""
    # if the texture already says the keywords below, say as-is    
    elif "print" in texture or "pattern" in texture:
        print_text = texture
    # otherwise, add 'print' after the texture
    else:
        print_text = texture + " print"
        
    return print_text

# CONSTRUCTING THE SENTENCES
# NOTE: color and type should always be present (unless there is a detection issue)
# therefore, sentence 1 will always result in a phrase, but sentence 2 may not

# Sentence 1
# General Form: “This is a” + color + style + “-style” + shape + fabric +  type + “.”
# e.g. This is a light pink, preppy-style, a-line, bow-front dress. 
def sent1():
    s1 = "This is"
    color_text = colors(color)
    s1 += a_an(color_text) + color_text
    attr()
    if (len(style) != 0):
        s1 += style + "-style" 
    if (len(shape) != 0):
        s1 += shape 
    if (len(fabric) != 0):
        s1 += fabric 
    if clothtype[0] == 2 and clothtype[1] != "skirt" and clothtype[1] != "sarong":
        s1 += " pair of"
    s1 += " " + clothtype[1] + "."
    print(s1)

# Sentence 2
# General Form: “It has” + texture + " and" + part_detail + “ detail.” 
# e.g. It has floral print and beaded-collar detail.
def sent2():
    s2 = ""
    if (len(texture) != 0 or len(part_detail) != 0):
        s2 = "It has"
        if (len(texture) != 0 and len(part_detail) != 0):
            s2 += print_or_not() + " and" + part_detail
        elif (len(part_detail) == 0):
            s2 += print_or_not()
        else:
            s2 += part_detail
        s2 += " detail."
    print(s2)
    
####################################
##### PRINTING EACH SENTENCE #######
####################################

sent1()
sent2()


