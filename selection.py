import maya.cmds as cmds

class Selection():
    def __init__(self,
                 render_geo_whitelist=["render"],
                 export_rig=False):

        self.selection_data = {}
        self.render_geo_whitelist = render_geo_whitelist
        self.export_rig = export_rig

        self.namespace = self.check_for_namespaces()

        characters, matching_groups = self.get_characters()

        for i, character in enumerate(characters):
            joint_grp_list = self.select_joint_grps(character)
            filtered_children, root_prim = self.get_geo_grps(group_name=matching_groups[i])

            temp_dict = {
                "root_prim": root_prim,
                "filtered_children": filtered_children,
                "joint_grp_path": joint_grp_list,
                "group_name": matching_groups[i],
                "namespace": self.namespace
            }

            self.selection_data[character] = temp_dict

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
            namespace = namespaces[0]
        else:
            namespace = None
        return namespace

    def get_characters(self):
        # formatting for namespaces and finds groups within rig structure
        if self.namespace:
            groups = cmds.ls(f"{self.namespace}:geo*", long=True)
        else:
            groups = cmds.ls("*geo*", long=True)

        matching_groups = []
        characters = []

        for grp in groups:
            parent = cmds.listRelatives(grp, parent=True, fullPath=True)
            if parent:
                parent_name = parent[0]
                if parent_name.endswith("rig"):
                    characters.append(parent_name)
                    matching_groups.append(grp)

        # tell user if _rig cannot be found
        if not characters and not matching_groups:
            cmds.warning("No parent group to geo found, make sure parent group of geo has _rig suffix \n")

        return (characters, matching_groups)

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
