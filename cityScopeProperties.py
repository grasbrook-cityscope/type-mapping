import enum


# main property keys
class PropertyKeys(enum.Enum):
    area_planning_type = "area_planning_type"
    land_use_general_type = "land_use_general_type"
    land_use_detail_type = "land_use_detail_type"


# building properties enums, to ensure properties use consistent keys
class BuildingDetailPropertyKeys(enum.Enum):
    building_id = "building_id"

    ground_floor_height = "building_base_height"
    building_height_total = "building_height"
    number_of_stories = "number_of_stories"
    additional_roof_height = "additional_roof_height"

    floor_area = "floor_area"
    area = "area"

    land_use_general_type = "land_use_general_type"
    land_use_detail_type = "land_use_detail_type"

    roof_type = "roof_type"

    secondary_use = "secondary_use"   # todo: wtf is this?


# highest level information: what is this?? building, open space, street , ...?
class AreaPlanningTypes(enum.Enum):
    street = "trafficArea"
    building = "building"
    open_space = "open_space"


# general use cases for buildings
class BuildingGeneralUse(enum.Enum):
    public = "public"
    commercial = "commercial"
    residential = "residential"
    special_use = "specialUse"
    daycare = "daycare"


# detail use cases for residential buildings
class BuildingDetailUsesResidential(enum.Enum):
    residential = "residential"

# detail use cases for commercial buildings
class BuildingDetailUsesCommercial(enum.Enum):
    commercial_office = "commercialOffice"
    light_industrial = "lightIndustrial"
    supermarket = "supermarket"
    store = "store"
    restaurant = "restaurant" # leisure
    kantine = "kantine" # leisure
    coffee = "coffee" # leisure
    sports_facility = "sportsFacility" # leisure


# detail use cases for public buildings
class BuildingDetailUsesPublic(enum.Enum):
    university = "university"
    kita = "kita"
    school = "school"
    library = "library"
    museum = "museum"
    habor_museum = "habor_museum"
    community_center = "community_center"
    health_center = "health_center"


# detail use cases for special use buildings   # todo: distinction of public use and special use not clear!
class BuildingDetailUsesSpecial(enum.Enum):
    creative_space = "creative_space"
    event_space = "event_space"
    religious = "religious"
    health_specialist = "health_specialist"
    sports_facility = "sports_facility"
    public_toilet = "public_toilet"


class BuildingDetailUses:
    residential_uses = BuildingDetailUsesResidential
    commercial_uses = BuildingDetailUsesCommercial
    public_uses = BuildingDetailUsesPublic
    special_uses = BuildingDetailUsesSpecial


# general uses of open spaces (looks more like ownership - this is a dept to HafenCity naming schemes)
class OpenSpaceGeneralUse(enum.Enum):
    public_open_space = "publicOS"
    private_open_space = "privateOS"
    semi_private_open_space = "semiPrivateOS"


# detail uses for open spaces
class OpenSpaceDetailUse(enum.Enum):
    park = "park"
    plaza = "plaza"
    promenade = "promenade"
    fire_parking = "fireParking"
    fire_access = "fireAccess"
    playground_school = "playgroundSchool"
    outdoor_gastronomy = "outdoorGastronomy"
    daycare_outdoor_area = "daycareOutdoorArea" # where is the difference to playground_kita??
    school_outdoor_area = "schoolOutdoorArea"
    playground_kita = "playgroundKita"
    sports_area = "sportsArea"


# general uses for area_planning_type = street
class StreetGeneralUse(enum.Enum):
    street = "street"

class StreetDetailUse(enum.Enum):
    street = "street"
    bridge = "bridge"


class RoofTypes(enum.Enum):
    extensive_green_roof = "extensive_green_roof"
    intensive_green_roof = "intensive_green_roof"
    normal_roof = "normal_roof"


class CityScopeItem():
    area_planning_type = None
    land_use_general_type = None
    land_use_detail_type = None
    detail_properties = {}

    def get_options_for_land_use_general_type(self):
        """Return Enum class with options for land use general type"""
        pass

    def get_options_for_land_use_detail_type(self):
        """Return Enum class with options for land use detailed type"""
        pass

    def get_options_for_detail_properties(self):
        """Return Enum class with options for detail properties"""
        pass

    def export_properties_to_json(self):
            json = {
                PropertyKeys.area_planning_type.value: self.area_planning_type.value,
                PropertyKeys.land_use_general_type.value: self.land_use_general_type.value,
                PropertyKeys.land_use_detail_type.value: self.land_use_detail_type.value,
            }

            for detail_prop_key, detail_prop_val in self.detail_properties.items():
                if detail_prop_val:
                    try:
                        json[detail_prop_key.value] = detail_prop_val.value
                    except:
                        json[detail_prop_key.value] = detail_prop_val

            return json


class CityScopeBuilding(CityScopeItem):

    area_planning_type = AreaPlanningTypes.building
    detail_properties = {
        BuildingDetailPropertyKeys.building_id: None,
        BuildingDetailPropertyKeys.ground_floor_height: None,
        BuildingDetailPropertyKeys.building_height_total: None,
        BuildingDetailPropertyKeys.number_of_stories: None,
        BuildingDetailPropertyKeys.additional_roof_height: None,
        BuildingDetailPropertyKeys.floor_area: None,
        BuildingDetailPropertyKeys.area: None,
        BuildingDetailPropertyKeys.land_use_general_type: None,
        BuildingDetailPropertyKeys.land_use_detail_type: None,
        BuildingDetailPropertyKeys.roof_type: None
    }


    def get_options_for_land_use_general_type(self):
        """Return Enum class with options for land use general type"""
        return BuildingGeneralUse

    def get_options_for_land_use_detail_type(self):
        """Return Enum class with options for land use detailed type"""
        if self.land_use_general_type == BuildingGeneralUse.public:
            return BuildingDetailUses.public_uses

        elif self.land_use_general_type == BuildingGeneralUse.residential:
            return BuildingDetailUses.residential_uses


        elif self.land_use_general_type == BuildingGeneralUse.commercial:
            return BuildingDetailUses.commercial_uses


        elif self.land_use_general_type == BuildingGeneralUse.special_use:
            return BuildingDetailUses.special_uses

        else:
            raise ValueError("land_use_general_type not set. Use one of ", self.get_options_for_land_use_general_type())


    def get_options_for_detail_properties(self):
        """Return Enum class with options for detail properties"""
        return BuildingDetailPropertyKeys


    def get_options_for_roof_types(self):
        """Return Enum class with options for roof types"""
        return RoofTypes


class CityScopeOpenSpace(CityScopeItem):

    area_planning_type = AreaPlanningTypes.open_space
    detail_properties = {
        # none yet , could be things like "soil_type"
    }

    def get_options_for_land_use_general_type(self):
        """Return Enum class with options for land use general type"""
        return OpenSpaceGeneralUse

    def get_options_for_land_use_detail_type(self):
        """Return Enum class with options for land use detailed type"""
        return OpenSpaceDetailUse

    def get_options_for_detail_properties(self):
        """Return Enum class with options for detail properties"""
        # detail properties for open spaces not defined yet
        return []


class CityScopeStreet(CityScopeItem):

    area_planning_type = AreaPlanningTypes.street
    detail_properties = {
        # none yet , could be "number_of_lanes"
    }

    def get_options_for_land_use_general_type(self):
        """Return Enum class with options for land use general type"""
        return StreetGeneralUse

    def get_options_for_land_use_detail_type(self):
        """Return Enum class with options for land use detailed type"""
        return StreetDetailUse

    def get_options_for_detail_properties(self):
        """Return Enum class with options for detail properties"""
        # detail properties for streets not defined yet
        return []




if __name__ == "__main__":

    print("*********************")
    print("*********************")

    # make new building
    building = CityScopeBuilding()
    building.land_use_general_type = building.get_options_for_land_use_general_type().commercial
    print("general use type", building.land_use_general_type)
    print("options for detailed use types", [o.value for o in building.get_options_for_land_use_detail_type()])

    building.land_use_detail_type = building.get_options_for_land_use_detail_type().commercial_office

    print("detailed use type", building.land_use_detail_type)

    # set some example detail property
    building.detail_properties[building.get_options_for_detail_properties().building_id] = 1234

    print("properties as json:      ")
    print(building.export_properties_to_json())





