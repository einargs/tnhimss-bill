import json
import pandas as pd
import re
from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.explanationofbenefit import ExplanationOfBenefit
from fhir.resources.R4B.allergyintolerance import AllergyIntolerance
from fhir.resources.R4B.appointment import Appointment
from fhir.resources.R4B.adverseevent import AdverseEvent
from fhir.resources.R4B.careplan import CarePlan
from fhir.resources.R4B.careteam import CareTeam
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.detectedissue import DetectedIssue
from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.familymemberhistory import FamilyMemberHistory
from fhir.resources.R4B.guidanceresponse import GuidanceResponse
from fhir.resources.R4B.imagingstudy import ImagingStudy
from fhir.resources.R4B.immunization import Immunization
from fhir.resources.R4B.immunizationrecommendation import ImmunizationRecommendation
from fhir.resources.R4B.medicationadministration import MedicationAdministration
from fhir.resources.R4B.medicationdispense import MedicationDispense
from fhir.resources.R4B.medicationrequest import MedicationRequest
from fhir.resources.R4B.medicationstatement import MedicationStatement
from fhir.resources.R4B.molecularsequence import MolecularSequence
from fhir.resources.R4B.person import Person
from fhir.resources.R4B.procedure import Procedure
from fhir.resources.R4B.provenance import Provenance
from fhir.resources.R4B.questionnaireresponse import QuestionnaireResponse
from fhir.resources.R4B.relatedperson import RelatedPerson
from fhir.resources.R4B.riskassessment import RiskAssessment
from fhir.resources.R4B.schedule import Schedule
from fhir.resources.R4B.specimen import Specimen
from fhir.resources.R4B.visionprescription import VisionPrescription
import pathlib