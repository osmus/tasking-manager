from schematics import Model
from schematics.exceptions import ValidationError
from schematics.types import (
    StringType,
    BaseType,
    IntType,
    BooleanType,
    FloatType,
    UTCDateTimeType,
    DateType,
)
from schematics.types.compound import ListType, ModelType
from backend.models.dtos.task_annotation_dto import TaskAnnotationDTO
from backend.models.dtos.stats_dto import Pagination
from backend.models.dtos.team_dto import ProjectTeamDTO
from backend.models.dtos.interests_dto import InterestDTO
from backend.models.postgis.statuses import (
    ProjectStatus,
    ProjectPriority,
    MappingTypes,
    TaskCreationMode,
    Editors,
    MappingPermission,
    ValidationPermission,
    ProjectDifficulty,
)
from backend.models.dtos.campaign_dto import CampaignDTO


def is_known_project_status(value):
    """Validates that Project Status is known value"""
    if isinstance(value, list):
        return  # Don't validate the entire list, just the individual values

    try:
        ProjectStatus[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown projectStatus: {value} Valid values are {ProjectStatus.DRAFT.name}, "
            f"{ProjectStatus.PUBLISHED.name}, {ProjectStatus.ARCHIVED.name}"
        )


def is_known_project_priority(value):
    """Validates Project priority is known value"""
    try:
        ProjectPriority[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown projectStatus: {value} Valid values are {ProjectPriority.LOW.name}, "
            f"{ProjectPriority.MEDIUM.name}, {ProjectPriority.HIGH.name}, "
            f"{ProjectPriority.URGENT.name}"
        )


def is_known_mapping_type(value):
    """Validates Mapping Type is known value"""
    if isinstance(value, list):
        return  # Don't validate the entire list, just the individual values

    try:
        MappingTypes[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown mappingType: {value} Valid values are {MappingTypes.ROADS.name}, "
            f"{MappingTypes.BUILDINGS.name}, {MappingTypes.WATERWAYS.name}, "
            f"{MappingTypes.LAND_USE.name}, {MappingTypes.OTHER.name}"
        )


def is_known_editor(value):
    """Validates Editor is known value"""
    if isinstance(value, list):
        return  # Don't validate the entire list, just the individual values

    try:
        Editors[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown editor: {value} Valid values are {Editors.ID.name}, "
            f"{Editors.JOSM.name}, {Editors.POTLATCH_2.name}, "
            f"{Editors.FIELD_PAPERS.name}, "
            f"{Editors.RAPID.name} "
        )


def is_known_task_creation_mode(value):
    """Validates Task Creation Mode is known value"""
    try:
        TaskCreationMode[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown taskCreationMode: {value} Valid values are {TaskCreationMode.GRID.name}, "
            f"{TaskCreationMode.ARBITRARY.name}"
        )


def is_known_mapping_permission(value):
    """Validates Mapping Permission String"""
    try:
        MappingPermission[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown mappingPermission: {value} Valid values are {MappingPermission.ANY.name}, "
            f"{MappingPermission.LEVEL.name}"
        )


def is_known_validation_permission(value):
    """Validates Validation Permission String"""
    try:
        ValidationPermission[value.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown validationPermission: {value} Valid values are {ValidationPermission.ANY.name}, "
            f"{ValidationPermission.LEVEL.name}, {ValidationPermission.TEAMS.name}, "
            f"{ValidationPermission.TEAMS_LEVEL.name}"
        )


def is_known_project_difficulty(value):
    """Validates that supplied project difficulty is known value"""
    if value.upper() == "ALL":
        return True

    try:
        value = value.split(",")
        for difficulty in value:
            ProjectDifficulty[difficulty.upper()]
    except KeyError:
        raise ValidationError(
            f"Unknown projectDifficulty: {value} Valid values are {ProjectDifficulty.EASY.name}, "
            f"{ProjectDifficulty.MODERATE.name}, {ProjectDifficulty.CHALLENGING.name} and ALL."
        )


class DraftProjectDTO(Model):
    """Describes JSON model used for creating draft project"""

    cloneFromProjectId = IntType(serialized_name="cloneFromProjectId")
    project_name = StringType(required=True, serialized_name="projectName")
    organisation = IntType(required=True)
    database = StringType(
        required=True,
        serialized_name="database",
        serialize_when_none=False,
    )
    area_of_interest = BaseType(required=True, serialized_name="areaOfInterest")
    tasks = BaseType(required=False)
    has_arbitrary_tasks = BooleanType(required=True, serialized_name="arbitraryTasks")
    user_id = IntType(required=True)


class ProjectInfoDTO(Model):
    """Contains the localized project info"""

    locale = StringType(required=True)
    name = StringType(default="")
    short_description = StringType(serialized_name="shortDescription", default="")
    description = StringType(default="")
    instructions = StringType(default="")
    per_task_instructions = StringType(
        default="", serialized_name="perTaskInstructions"
    )


class CustomEditorDTO(Model):
    """DTO to define a custom editor"""

    name = StringType(required=True)
    description = StringType()
    url = StringType(required=True)


class ProjectDTO(Model):
    """Describes JSON model for a tasking manager project"""

    project_id = IntType(serialized_name="projectId")
    database = StringType(
        required=True,
        serialized_name="database",
        serialize_when_none=False,
    )
    project_status = StringType(
        required=True,
        serialized_name="status",
        validators=[is_known_project_status],
        serialize_when_none=False,
    )
    project_priority = StringType(
        required=True,
        serialized_name="projectPriority",
        validators=[is_known_project_priority],
        serialize_when_none=False,
    )
    area_of_interest = BaseType(serialized_name="areaOfInterest")
    aoi_bbox = ListType(FloatType, serialized_name="aoiBBOX")
    tasks = BaseType(serialize_when_none=False)
    default_locale = StringType(
        required=True, serialized_name="defaultLocale", serialize_when_none=False
    )
    project_info = ModelType(
        ProjectInfoDTO, serialized_name="projectInfo", serialize_when_none=False
    )
    project_info_locales = ListType(
        ModelType(ProjectInfoDTO),
        serialized_name="projectInfoLocales",
        serialize_when_none=False,
    )
    difficulty = StringType(
        required=True,
        serialized_name="difficulty",
        validators=[is_known_project_difficulty],
    )
    mapping_permission = StringType(
        required=True,
        serialized_name="mappingPermission",
        validators=[is_known_mapping_permission],
    )
    validation_permission = StringType(
        required=True,
        serialized_name="validationPermission",
        validators=[is_known_validation_permission],
    )
    enforce_random_task_selection = BooleanType(
        required=False, default=False, serialized_name="enforceRandomTaskSelection"
    )

    private = BooleanType(required=True)
    changeset_comment = StringType(serialized_name="changesetComment")
    osmcha_filter_id = StringType(serialized_name="osmchaFilterId")
    due_date = UTCDateTimeType(serialized_name="dueDate")
    imagery = StringType()
    josm_preset = StringType(serialized_name="josmPreset", serialize_when_none=False)
    id_presets = ListType(StringType, serialized_name="idPresets", default=[])
    extra_id_params = StringType(serialized_name="extraIdParams")
    rapid_power_user = BooleanType(
        serialized_name="rapidPowerUser", default=False, required=False
    )
    mapping_types = ListType(
        StringType,
        serialized_name="mappingTypes",
        default=[],
        validators=[is_known_mapping_type],
    )
    campaigns = ListType(ModelType(CampaignDTO), default=[])
    organisation = IntType(required=True)
    organisation_name = StringType(serialized_name="organisationName")
    organisation_slug = StringType(serialized_name="organisationSlug")
    organisation_logo = StringType(serialized_name="organisationLogo")
    country_tag = ListType(StringType, serialized_name="countryTag")

    license_id = IntType(serialized_name="licenseId")
    allowed_usernames = ListType(
        StringType(), serialized_name="allowedUsernames", default=[]
    )
    priority_areas = BaseType(serialized_name="priorityAreas")
    created = UTCDateTimeType()
    last_updated = UTCDateTimeType(serialized_name="lastUpdated")
    author = StringType()
    active_mappers = IntType(serialized_name="activeMappers")
    percent_mapped = IntType(serialized_name="percentMapped")
    percent_validated = IntType(serialized_name="percentValidated")
    percent_bad_imagery = IntType(serialized_name="percentBadImagery")
    task_creation_mode = StringType(
        required=True,
        serialized_name="taskCreationMode",
        validators=[is_known_task_creation_mode],
        serialize_when_none=False,
    )
    project_teams = ListType(ModelType(ProjectTeamDTO), serialized_name="teams")
    mapping_editors = ListType(
        StringType,
        min_size=1,
        required=True,
        serialized_name="mappingEditors",
        validators=[is_known_editor],
    )
    validation_editors = ListType(
        StringType,
        min_size=1,
        required=True,
        serialized_name="validationEditors",
        validators=[is_known_editor],
    )
    custom_editor = ModelType(
        CustomEditorDTO, serialized_name="customEditor", serialize_when_none=False
    )
    interests = ListType(ModelType(InterestDTO))


class ProjectFavoriteDTO(Model):
    """DTO used to favorite a project"""

    project_id = IntType(required=True)
    user_id = IntType(required=True)


class ProjectFavoritesDTO(Model):
    """DTO to retrieve favorited projects"""

    def __init__(self):
        super().__init__()
        self.favorited_projects = []

    favorited_projects = ListType(
        ModelType(ProjectDTO), serialized_name="favoritedProjects"
    )


class ProjectSearchDTO(Model):
    """Describes the criteria users use to filter active projects"""

    preferred_locale = StringType(default="en")
    difficulty = StringType(validators=[is_known_project_difficulty])
    database = StringType()
    action = StringType()
    mapping_types = ListType(StringType, validators=[is_known_mapping_type])
    mapping_types_exact = BooleanType(required=False)
    project_statuses = ListType(StringType, validators=[is_known_project_status])
    organisation_name = StringType()
    organisation_id = IntType()
    team_id = IntType()
    campaign = StringType()
    order_by = StringType()
    order_by_type = StringType()
    country = StringType()
    page = IntType(required=True)
    text_search = StringType()
    mapping_editors = ListType(StringType, validators=[is_known_editor])
    validation_editors = ListType(StringType, validators=[is_known_editor])
    teams = ListType(StringType())
    interests = ListType(IntType())
    created_by = IntType(required=False)
    mapped_by = IntType(required=False)
    favorited_by = IntType(required=False)
    managed_by = IntType(required=False)
    based_on_user_interests = IntType(required=False)
    omit_map_results = BooleanType(required=False)
    last_updated_lte = StringType(required=False)
    last_updated_gte = StringType(required=False)
    created_lte = StringType(required=False)
    created_gte = StringType(required=False)

    def __hash__(self):
        """Make object hashable so we can cache user searches"""
        hashable_mapping_types = ""
        if self.mapping_types:
            for mapping_type in self.mapping_types:
                hashable_mapping_types += mapping_type
        hashable_project_statuses = ""
        if self.project_statuses:
            for project_status in self.project_statuses:
                hashable_project_statuses += project_status
        hashable_teams = ""
        if self.teams:
            for team in self.teams:
                hashable_teams += team
        hashable_mapping_editors = ""
        if self.mapping_editors:
            for mapping_editor in self.mapping_editors:
                hashable_mapping_editors = hashable_mapping_editors + mapping_editor
        hashable_validation_editors = ""
        if self.validation_editors:
            for validation_editor in self.validation_editors:
                hashable_validation_editors = (
                    hashable_validation_editors + validation_editor
                )

        return hash(
            (
                self.preferred_locale,
                self.database,
                self.difficulty,
                hashable_mapping_types,
                hashable_project_statuses,
                hashable_teams,
                self.organisation_name,
                self.campaign,
                self.page,
                self.text_search,
                hashable_mapping_editors,
                hashable_validation_editors,
                self.created_by,
            )
        )


class ProjectSearchBBoxDTO(Model):
    bbox = ListType(FloatType, required=True, min_size=4, max_size=4)
    input_srid = IntType(required=True, choices=[4326])
    preferred_locale = StringType(required=False, default="en")
    project_author = IntType(required=False, serialized_name="projectAuthor")


class ListSearchResultDTO(Model):
    """Describes one search result"""

    project_id = IntType(required=True, serialized_name="projectId")
    locale = StringType(required=True)
    name = StringType(default="")
    short_description = StringType(serialized_name="shortDescription", default="")
    database = StringType(required=True, serialized_name="database")
    difficulty = StringType(required=True, serialized_name="difficulty")
    priority = StringType(required=True)
    organisation_name = StringType(serialized_name="organisationName")
    organisation_logo = StringType(serialized_name="organisationLogo")
    campaigns = ListType(ModelType(CampaignDTO), default=[])
    percent_mapped = IntType(serialized_name="percentMapped")
    percent_validated = IntType(serialized_name="percentValidated")
    status = StringType(serialized_name="status")
    active_mappers = IntType(serialized_name="activeMappers")
    last_updated = UTCDateTimeType(serialized_name="lastUpdated")
    due_date = UTCDateTimeType(serialized_name="dueDate")
    total_contributors = IntType(serialized_name="totalContributors")
    country = StringType(serialize_when_none=False)


class ProjectSearchResultsDTO(Model):
    """Contains all results for the search criteria"""

    def __init__(self):
        """DTO constructor initialise all arrays to empty"""
        super().__init__()
        self.results = []
        self.map_results = []

    map_results = BaseType(serialized_name="mapResults")
    results = ListType(ModelType(ListSearchResultDTO))
    pagination = ModelType(Pagination)


class LockedTasksForUser(Model):
    """Describes all tasks locked by an individual user"""

    def __init__(self):
        """DTO constructor initialise all arrays to empty"""
        super().__init__()
        self.locked_tasks = []

    locked_tasks = ListType(IntType, serialized_name="lockedTasks")
    project = IntType(serialized_name="projectId")
    task_status = StringType(serialized_name="taskStatus")


class ProjectComment(Model):
    """Describes an individual user comment on a project task"""

    comment = StringType()
    comment_date = UTCDateTimeType(serialized_name="commentDate")
    user_name = StringType(serialized_name="userName")
    task_id = IntType(serialized_name="taskId")


class ProjectCommentsDTO(Model):
    """Contains all comments on a project"""

    def __init__(self):
        """DTO constructor initialise all arrays to empty"""
        super().__init__()
        self.comments = []

    comments = ListType(ModelType(ProjectComment))


class ProjectContribDTO(Model):
    date = DateType(required=True)
    mapped = IntType(required=True)
    validated = IntType(required=True)
    cumulative_mapped = IntType(required=False)
    cumulative_validated = IntType(required=False)
    total_tasks = IntType(required=False)


class ProjectContribsDTO(Model):
    """Contains all contributions on a project by day"""

    def __init__(self):
        """DTO constructor initialise all arrays to empty"""
        super().__init__()
        self.mapping = []
        self.validation = []

    stats = ListType(ModelType(ProjectContribDTO))


class ProjectSummary(Model):
    """Model used for PM dashboard"""

    project_id = IntType(required=True, serialized_name="projectId")
    default_locale = StringType(serialized_name="defaultLocale")
    author = StringType()
    created = UTCDateTimeType()
    due_date = UTCDateTimeType(serialized_name="dueDate")
    last_updated = UTCDateTimeType(serialized_name="lastUpdated")
    priority = StringType(serialized_name="projectPriority")
    campaigns = ListType(ModelType(CampaignDTO), default=[])
    organisation = IntType()
    organisation_name = StringType(serialized_name="organisationName")
    organisation_slug = StringType(serialized_name="organisationSlug")
    organisation_logo = StringType(serialized_name="organisationLogo")
    country_tag = ListType(StringType, serialized_name="countryTag")
    osmcha_filter_id = StringType(serialized_name="osmchaFilterId")
    mapping_types = ListType(
        StringType, serialized_name="mappingTypes", validators=[is_known_mapping_type]
    )

    changeset_comment = StringType(serialized_name="changesetComment")
    percent_mapped = IntType(serialized_name="percentMapped")
    percent_validated = IntType(serialized_name="percentValidated")
    percent_bad_imagery = IntType(serialized_name="percentBadImagery")
    aoi_centroid = BaseType(serialized_name="aoiCentroid")
    database = StringType(serialized_name="database")
    difficulty = StringType(serialized_name="difficulty")
    mapping_permission = IntType(
        serialized_name="mappingPermission", validators=[is_known_mapping_permission]
    )
    validation_permission = IntType(
        serialized_name="validationPermission",
        validators=[is_known_validation_permission],
    )
    allowed_usernames = ListType(
        StringType(), serialized_name="allowedUsernames", default=[]
    )
    random_task_selection_enforced = BooleanType(
        required=False, default=False, serialized_name="enforceRandomTaskSelection"
    )
    private = BooleanType(serialized_name="private")
    allowed_users = ListType(StringType, serialized_name="allowedUsernames", default=[])
    project_teams = ListType(ModelType(ProjectTeamDTO), serialized_name="teams")
    project_info = ModelType(
        ProjectInfoDTO, serialized_name="projectInfo", serialize_when_none=False
    )
    short_description = StringType(serialized_name="shortDescription")
    status = StringType()
    imagery = StringType()
    license_id = IntType(serialized_name="licenseId")
    id_presets = ListType(StringType, serialized_name="idPresets", default=[])
    extra_id_params = StringType(serialized_name="extraIdParams")
    rapid_power_user = BooleanType(
        serialized_name="rapidPowerUser", default=False, required=False
    )
    mapping_editors = ListType(
        StringType,
        min_size=1,
        required=True,
        serialized_name="mappingEditors",
        validators=[is_known_editor],
    )
    validation_editors = ListType(
        StringType,
        min_size=1,
        required=True,
        serialized_name="validationEditors",
        validators=[is_known_editor],
    )
    custom_editor = ModelType(
        CustomEditorDTO, serialized_name="customEditor", serialize_when_none=False
    )


class PMDashboardDTO(Model):
    """DTO for constructing the PM Dashboard"""

    def __init__(self):
        """DTO constructor initialise all arrays to empty"""
        super().__init__()
        self.draft_projects = []
        self.archived_projects = []
        self.active_projects = []

    draft_projects = ListType(
        ModelType(ProjectSummary), serialized_name="draftProjects"
    )
    active_projects = ListType(
        ModelType(ProjectSummary), serialized_name="activeProjects"
    )
    archived_projects = ListType(
        ModelType(ProjectSummary), serialized_name="archivedProjects"
    )


class ProjectTaskAnnotationsDTO(Model):
    """DTO for task annotations of a project"""

    def __init__(self):
        """DTO constructor set task arrays to empty"""
        super().__init__()
        self.tasks = []

    project_id = IntType(required=True, serialized_name="projectId")
    tasks = ListType(
        ModelType(TaskAnnotationDTO), required=True, serialized_name="tasks"
    )


class ProjectStatsDTO(Model):
    """DTO for detailed stats on a project"""

    project_id = IntType(required=True, serialized_name="projectId")
    area = FloatType(serialized_name="projectArea(in sq.km)")
    total_mappers = IntType(serialized_name="totalMappers")
    total_tasks = IntType(serialized_name="totalTasks")
    total_comments = IntType(serialized_name="totalComments")
    total_mapping_time = IntType(serialized_name="totalMappingTime")
    total_validation_time = IntType(serialized_name="totalValidationTime")
    total_time_spent = IntType(serialized_name="totalTimeSpent")
    average_mapping_time = IntType(serialized_name="averageMappingTime")
    average_validation_time = IntType(serialized_name="averageValidationTime")
    percent_mapped = IntType(serialized_name="percentMapped")
    percent_validated = IntType(serialized_name="percentValidated")
    percent_bad_imagery = IntType(serialized_name="percentBadImagery")
    aoi_centroid = BaseType(serialized_name="aoiCentroid")
    time_to_finish_mapping = IntType(serialized_name="timeToFinishMapping")
    time_to_finish_validating = IntType(serialized_name="timeToFinishValidating")


class ProjectUserStatsDTO(Model):
    """DTO for time spent by users on a project"""

    time_spent_mapping = IntType(serialized_name="timeSpentMapping")
    time_spent_validating = IntType(serialized_name="timeSpentValidating")
    total_time_spent = IntType(serialized_name="totalTimeSpent")
