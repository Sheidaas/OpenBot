import item
def debugprint(arg):
    """
    Log's information to Log.txt file. This will Not print time.

    Args:
        arg ([str]): Information to log.
    """
    with open(eXLib.PATH+"\\item_IdTypeIconName_tr.txt","a") as f:
        f.write(str(arg)+"\n")

debugprint("ID Type Icon")

for i in range(165500):
    if item.SelectItem(i) == 1:
        id = i
        i_type = item.GetItemType()
        iconName = item.GetIconImageFileName().replace("icon\item\\", '').replace('.tga', '')
        itemName = item.GetItemName()
        if not iconName == "" and not i_type == 0 and not itemName == "":
            debugprint(str(i)+ "," + str(i_type) + "," + str(iconName) + "," + str(itemName))
