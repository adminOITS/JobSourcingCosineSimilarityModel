from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class SkillProficiencyLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    MASTER = "MASTER"

class RequirementLevel(str, Enum):
    REQUIRED = "REQUIRED"
    OPTIONAL = "OPTIONAL"
    PREFERRED = "PREFERRED"

class OfferProficiencyLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    FLUENT = "FLUENT"
    NATIVE = "NATIVE"
    BASIC = "BASIC"

class LanguageProficiencyLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    NATIVE = "NATIVE"

@dataclass
class CandidateSkillResponseDto:
    name: str
    proficiencyLevel: SkillProficiencyLevel

@dataclass
class JobOfferSkillResponseDto:
    skillName: str
    proficiency: OfferProficiencyLevel
    requirementLevel: RequirementLevel

@dataclass
class JobOfferExperienceResponseDto:
    title: str
    companyName: Optional[str]
    description: Optional[str]
    yearsRequired: Optional[int]
    requirementLevel: RequirementLevel

@dataclass
class CandidateExperienceResponseDto:
    jobTitle: str
    company: Optional[str]
    startDate: Optional[str]  # "YYYY-MM-DD"
    endDate: Optional[str]    # "YYYY-MM-DD"
    isCurrent: bool
    description: Optional[str]
    location: Optional[str]
    industry: Optional[str]

@dataclass
class JobOfferEducationResponseDto:
    degree: str
    field: Optional[str]
    institution: Optional[str]
    requirementLevel: RequirementLevel
    description: Optional[str]

@dataclass
class CandidateEducationResponseDto:
    degree: str
    field: Optional[str]
    institution: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    isCurrent: bool
    location: Optional[str]

@dataclass
class JobOfferLanguageResponseDto:
    language: str
    proficiency: LanguageProficiencyLevel
    requirementLevel: RequirementLevel

@dataclass
class CandidateLanguageResponseDto:
    language: str
    proficiencyLevel: LanguageProficiencyLevel

@dataclass
class AddressResponseDto:
    addressLine1: str
    addressLine2: str
    city: str
    state: str
    zipCode: str
    country: str

@dataclass
class CandidateResponseDto:
    address: Optional[AddressResponseDto]
    experiences: List[CandidateExperienceResponseDto]
    education: List[CandidateEducationResponseDto]
    languages: List[CandidateLanguageResponseDto]

@dataclass
class ProfileResponseDto:
    profileTitle: str
    category: Optional[str]
    candidate: CandidateResponseDto
    skills: List[CandidateSkillResponseDto]

@dataclass
class JobOfferResponseDto:
    title: str
    category: Optional[str]
    city: Optional[str]
    country: Optional[str]
    zipCode: Optional[str]
    skills: List[JobOfferSkillResponseDto]
    experiences: List[JobOfferExperienceResponseDto]
    educations: List[JobOfferEducationResponseDto]
    languages: List[JobOfferLanguageResponseDto]
