import maya.cmds as cmds

class Selection():
    def __init__(self,
                 render_geo_whitelist=["render"],
                 export_rig=False):

        self.selection_data = {}
        self.render_geo_whitelist = render_geo_whitelist
        self.export_rig = export_rig

        self.namespaces = self.check_for_namespaces()

        character_dict = self.get_characters()

        for character in character_dict.values():
            self.namespace = character["namespace"]
            joint_grp_list = self.select_joint_grps(character["character_name"])
            filtered_children, root_prim = self.get_geo_grps(group_name=character["matching_groups"])

            temp_dict = {
                "root_prim": root_prim,
                "filtered_children": filtered_children,
                "joint_grp_path": joint_grp_list,
                "group_name": character["matching_groups"],
                "namespace": self.namespace
            }

            self.selection_data[character["character_name"]] = temp_dict

    def select_joint_grps(self, character):
        joint_grp_list = []
        if self.export_rig is True:
            for joint_grp in self.get_joint_grps(f"{character}_rig"):
                joint_grp_list.append(joint_grp)
            return joint_grp_list

    def check_for_namespaces(self):
        # check for existing namespaces and remove mayas constant namespaces
        namespaces = cmds.namespaceInfo(lon=True, r=True)
        if "UI" and "shared" in namespaces:
            namespaces.remove("UI")
            namespaces.remove("shared")

        # formatting for namespaces
        if namespaces:
            return namespaces
        else:
            return None

    def get_characters(self):
        character_dict = {}
        groups = []
        
        # formatting for namespaces and finds groups within rig structure
        if self.namespaces:
            for namespace in self.namespaces:
                if cmds.ls(f"{namespace}:geo", long=True):
                    group = cmds.ls(f"{namespace}:geo", long=True)
                    groups.append(group[0])
            if not groups:  # other namespaces can exist in maya scenes this catches that error
                groups.append(cmds.ls("geo", long=True)[0])
        else:

            groups.append(cmds.ls("geo", long=True)[0])
        
        for grp in groups:
            parent = cmds.listRelatives(grp, parent=True, fullPath=True)
            if parent:
                parent_name = parent[0]
                if parent_name.endswith("rig"):
                    namespace = parent_name.rpartition(":")[0]
                    namespace = namespace.replace("|","")
                    if not namespace:
                        namespace = None
                    character_dict[parent_name] = {
                        "matching_groups": grp,
                        "character_name": parent_name,
                        "namespace": namespace
                        }

        # tell user if _rig cannot be found
        if not character_dict:
            cmds.warning("No parent group to geo found, make sure parent group of geo has _rig suffix \n")
        
        return character_dict

    def get_geo_grps(self, group_name):
        #find root and child groups/prims and filter these through specified groups per to export
        root_prim = cmds.listRelatives(group_name, parent=True)[0]
        children = cmds.listRelatives(group_name, children=True)

        if self.namespace:
            for geo in self.render_geo_whitelist:
                new_geo = f"{self.namespace}:{geo}"
                index = self.render_geo_whitelist.index(geo)
                self.render_geo_whitelist[index] = new_geo

        filtered_children = [
            child for child in children if child in self.render_geo_whitelist
        ]
        if len(filtered_children) == 0:
            return
        return (filtered_children, root_prim)

    def get_joint_grps(self, character):
        # find the joints and joint groups within the rig structure
        def traverse(parent_path):
            # traverse filters through children of character to find grp with "joints_grp" attr
            attr_name = "joints_grp"
            found_items = []
            try:
                children = cmds.listRelatives(parent_path, children=True, fullPath=True)
            except ValueError:
                cmds.warning("grp_joints does not exist under character")
                return found_items

            if not children:
                return found_items

            # checks each child for existing obj and attr
            for child in children:
                attr_path = child+"."+attr_name
                # appends joint grp if they have attr_path on the joints grp (allows you only to export skin joints)
                try:
                    if cmds.objExists(child) == True and cmds.getAttr(attr_path, asString=True) == "True":
                        found_items.append(child)
                except ValueError: 
                    pass
                
                # if a child found traverse the child again until no more children
                child_found_items = traverse(child)
                found_items.extend(child_found_items)

            return found_items

        # apply namespace data if it exists
        if self.namespace:
            joints_path = f"{character}|{self.namespace}:grp_joints"  # parent group to joints grp
        else:
            joints_path = f"{character}|grp_joints"
        character_paths = traverse(joints_path)
        return character_paths

    def return_data(self):
        return self.selection_data
