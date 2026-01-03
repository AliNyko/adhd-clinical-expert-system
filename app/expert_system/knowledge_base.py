"""Clinical Knowledge Base for ADHD, Depression, and Anxiety Assessment.

This module contains expert-level clinical knowledge extracted from:
- DSM-5-TR diagnostic criteria
- ICD-11 guidelines
- Peer-reviewed clinical research
- Real-world clinical practice patterns
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class SymptomCluster:
    """Represents a cluster of related symptoms for a condition."""
    name: str
    symptoms: List[str]
    weight: float  # Clinical significance weight (0.0 to 1.0)
    context_dependent: bool = False
    developmental_pattern: str = ""  # "childhood-onset", "episodic", "chronic"


@dataclass
class DiagnosticCriteria:
    """Complete diagnostic criteria for a clinical condition."""
    condition: str
    primary_clusters: List[SymptomCluster]
    exclusion_criteria: List[str]
    duration_requirement: str
    onset_requirement: str
    functional_impairment_required: bool
    context_requirements: List[str]


class ClinicalKnowledgeBase:
    """Expert clinical knowledge base for differential diagnosis."""
    
    def __init__(self):
        """Initialize the clinical knowledge base."""
        self.adhd_criteria = self._build_adhd_criteria()
        self.depression_criteria = self._build_depression_criteria()
        self.anxiety_criteria = self._build_anxiety_criteria()
        self.differential_markers = self._build_differential_markers()
        self.comorbidity_patterns = self._build_comorbidity_patterns()
        
    def _build_adhd_criteria(self) -> DiagnosticCriteria:
        """Build ADHD diagnostic criteria based on DSM-5-TR."""
        
        inattention_cluster = SymptomCluster(
            name="Inattention",
            symptoms=[
                "fails_to_give_close_attention_to_details",
                "difficulty_sustaining_attention",
                "does_not_seem_to_listen",
                "does_not_follow_through_instructions",
                "difficulty_organizing_tasks",
                "avoids_sustained_mental_effort",
                "loses_things_necessary_for_tasks",
                "easily_distracted_by_extraneous_stimuli",
                "forgetful_in_daily_activities"
            ],
            weight=1.0,
            context_dependent=True,
            developmental_pattern="childhood-onset"
        )
        
        hyperactivity_impulsivity_cluster = SymptomCluster(
            name="Hyperactivity-Impulsivity",
            symptoms=[
                "fidgets_with_hands_or_feet",
                "leaves_seat_when_remaining_seated_expected",
                "feels_restless",
                "difficulty_engaging_in_leisure_quietly",
                "on_the_go_driven_by_motor",
                "talks_excessively",
                "blurts_out_answers",
                "difficulty_waiting_turn",
                "interrupts_or_intrudes_on_others"
            ],
            weight=1.0,
            context_dependent=True,
            developmental_pattern="childhood-onset"
        )
        
        return DiagnosticCriteria(
            condition="ADHD",
            primary_clusters=[inattention_cluster, hyperactivity_impulsivity_cluster],
            exclusion_criteria=[
                "symptoms_better_explained_by_another_mental_disorder",
                "symptoms_only_during_psychosis"
            ],
            duration_requirement="at_least_6_months",
            onset_requirement="symptoms_present_before_age_12",
            functional_impairment_required=True,
            context_requirements=["two_or_more_settings"]
        )
    
    def _build_depression_criteria(self) -> DiagnosticCriteria:
        """Build Major Depressive Disorder criteria based on DSM-5-TR."""
        
        core_depression_cluster = SymptomCluster(
            name="Core Depressive Symptoms",
            symptoms=[
                "depressed_mood_most_of_day",
                "markedly_diminished_interest_or_pleasure",
                "significant_weight_change_or_appetite_change",
                "insomnia_or_hypersomnia",
                "psychomotor_agitation_or_retardation",
                "fatigue_or_loss_of_energy",
                "feelings_of_worthlessness_or_guilt",
                "diminished_ability_to_think_or_concentrate",
                "recurrent_thoughts_of_death_or_suicide"
            ],
            weight=1.0,
            context_dependent=False,
            developmental_pattern="episodic"
        )
        
        return DiagnosticCriteria(
            condition="Major Depressive Disorder",
            primary_clusters=[core_depression_cluster],
            exclusion_criteria=[
                "symptoms_due_to_substance_or_medical_condition",
                "manic_or_hypomanic_episode_ever"
            ],
            duration_requirement="at_least_2_weeks",
            onset_requirement="no_specific_childhood_onset_required",
            functional_impairment_required=True,
            context_requirements=["nearly_every_day_during_episode"]
        )
    
    def _build_anxiety_criteria(self) -> DiagnosticCriteria:
        """Build Generalized Anxiety Disorder criteria based on DSM-5-TR."""
        
        core_anxiety_cluster = SymptomCluster(
            name="Core Anxiety Symptoms",
            symptoms=[
                "excessive_anxiety_and_worry",
                "difficulty_controlling_worry",
                "restlessness_or_feeling_on_edge",
                "being_easily_fatigued",
                "difficulty_concentrating_mind_going_blank",
                "irritability",
                "muscle_tension",
                "sleep_disturbance"
            ],
            weight=1.0,
            context_dependent=False,
            developmental_pattern="chronic"
        )
        
        return DiagnosticCriteria(
            condition="Generalized Anxiety Disorder",
            primary_clusters=[core_anxiety_cluster],
            exclusion_criteria=[
                "anxiety_due_to_substance_or_medical_condition",
                "anxiety_better_explained_by_another_anxiety_disorder"
            ],
            duration_requirement="at_least_6_months",
            onset_requirement="no_specific_childhood_onset_required",
            functional_impairment_required=True,
            context_requirements=["more_days_than_not"]
        )
    
    def _build_differential_markers(self) -> Dict[str, Dict[str, Any]]:
        """Build markers that help differentiate between conditions.
        
        These are expert-level clinical heuristics used by experienced clinicians
        to distinguish between similar-appearing conditions.
        """
        return {
            "adhd_vs_depression": {
                "adhd_favoring": [
                    "symptoms_present_since_childhood",
                    "consistent_across_lifespan",
                    "executive_dysfunction_primary",
                    "stimulus_seeking_behavior",
                    "difficulty_with_organization_time_management",
                    "no_clear_mood_episodes",
                    "restlessness_driven_by_motor",
                    "impulsivity_not_mood_related"
                ],
                "depression_favoring": [
                    "episodic_pattern_with_clear_onset",
                    "anhedonia_and_depressed_mood_primary",
                    "cognitive_slowing_due_to_mood",
                    "loss_of_interest_in_previously_enjoyed_activities",
                    "guilt_and_worthlessness_prominent",
                    "sleep_and_appetite_changes",
                    "symptoms_worse_at_specific_times_of_day",
                    "no_childhood_adhd_history"
                ],
                "clinical_reasoning": [
                    "Depression causes secondary attention problems; ADHD is primary",
                    "ADHD symptoms are lifelong and consistent; depression is episodic",
                    "In depression, concentration improves when mood lifts",
                    "ADHD shows poor sustained attention even during positive activities"
                ]
            },
            "adhd_vs_anxiety": {
                "adhd_favoring": [
                    "distractibility_not_due_to_worry",
                    "impulsivity_and_risk_taking",
                    "hyperactivity_not_tension_related",
                    "poor_follow_through_on_tasks",
                    "disorganization_primary",
                    "childhood_onset_before_anxiety",
                    "no_specific_worry_content"
                ],
                "anxiety_favoring": [
                    "attention_problems_only_when_anxious",
                    "restlessness_due_to_worry_and_tension",
                    "specific_worry_themes_identifiable",
                    "avoidance_behaviors_present",
                    "physical_tension_and_muscle_aches",
                    "perfectionism_and_over_checking",
                    "symptoms_fluctuate_with_stress_level"
                ],
                "clinical_reasoning": [
                    "Anxiety causes worry-focused attention; ADHD is diffuse inattention",
                    "Anxiety restlessness is tense; ADHD restlessness is driven",
                    "ADHD shows poor inhibition; anxiety shows over-control",
                    "Family history: ADHD is more heritable than GAD"
                ]
            },
            "depression_vs_anxiety": {
                "depression_favoring": [
                    "anhedonia_more_prominent_than_worry",
                    "psychomotor_retardation",
                    "early_morning_awakening",
                    "diurnal_mood_variation",
                    "guilt_prominent"
                ],
                "anxiety_favoring": [
                    "worry_more_prominent_than_mood_low",
                    "hypervigilance",
                    "difficulty_falling_asleep",
                    "physical_tension_prominent",
                    "anticipatory_anxiety"
                ],
                "clinical_reasoning": [
                    "Depression and anxiety frequently co-occur",
                    "Assess which came first and which is more impairing",
                    "PHQ-9 and GAD-7 scores help quantify relative severity"
                ]
            }
        }
    
    def _build_comorbidity_patterns(self) -> Dict[str, Any]:
        """Build knowledge about common comorbidity patterns.
        
        Based on clinical research showing high rates of co-occurrence.
        """
        return {
            "adhd_depression": {
                "prevalence": "30-50% of adults with ADHD have comorbid depression",
                "clinical_pattern": [
                    "ADHD typically predates depression onset",
                    "Chronic ADHD impairment can lead to secondary depression",
                    "Depression can unmask previously compensated ADHD",
                    "Both require treatment for optimal outcomes"
                ],
                "differential_challenge": "Both cause concentration problems",
                "key_distinction": "ADHD attention problems are lifelong; depression is episodic"
            },
            "adhd_anxiety": {
                "prevalence": "25-40% of adults with ADHD have comorbid anxiety",
                "clinical_pattern": [
                    "ADHD often leads to secondary anxiety due to failures",
                    "Anxiety can worsen ADHD symptom expression",
                    "Performance anxiety common in undiagnosed ADHD",
                    "Social anxiety from chronic interpersonal difficulties"
                ],
                "differential_challenge": "Both cause restlessness and concentration problems",
                "key_distinction": "ADHD restlessness is motoric; anxiety is tense worry"
            },
            "depression_anxiety": {
                "prevalence": "60-70% comorbidity rate",
                "clinical_pattern": [
                    "Often occur together as part of common underlying vulnerability",
                    "Anxiety typically predates depression",
                    "Mixed anxiety-depression is common presentation",
                    "PHQ-ADS score helps assess combined burden"
                ],
                "differential_challenge": "Overlapping cognitive and vegetative symptoms",
                "key_distinction": "Assess predominant affect: low mood vs. worry"
            },
            "triple_comorbidity": {
                "prevalence": "10-20% of ADHD cases",
                "clinical_pattern": [
                    "ADHD as primary neurodevelopmental condition",
                    "Secondary depression and anxiety from chronic impairment",
                    "Complex presentation requiring careful assessment",
                    "Requires integrated treatment approach"
                ],
                "assessment_strategy": [
                    "Establish childhood ADHD history first",
                    "Map timeline of depression and anxiety onset",
                    "Assess each condition's relative contribution to impairment",
                    "Consider sequential or concurrent treatment"
                ]
            }
        }
    
    def get_validated_scales_info(self) -> Dict[str, Any]:
        """Return information about validated assessment scales."""
        return {
            "ASRS_v1_1": {
                "name": "Adult ADHD Self-Report Scale",
                "purpose": "ADHD symptom screening in adults",
                "parts": {
                    "Part_A": {
                        "items": 6,
                        "description": "Most predictive symptoms",
                        "scoring": "4+ symptoms in shaded zone = positive screen",
                        "clinical_note": "High sensitivity but requires clinical follow-up"
                    },
                    "Part_B": {
                        "items": 12,
                        "description": "Additional symptoms for comprehensive assessment",
                        "scoring": "Total score 0-72",
                        "clinical_note": "Provides symptom severity estimate"
                    }
                },
                "interpretation": [
                    "Positive screen is NOT a diagnosis",
                    "Requires clinical interview to confirm DSM-5-TR criteria",
                    "Must assess childhood onset and current impairment",
                    "Consider differential diagnoses"
                ]
            },
            "PHQ_9": {
                "name": "Patient Health Questionnaire-9",
                "purpose": "Depression severity screening",
                "scoring": {
                    "range": "0-27",
                    "minimal": "0-4",
                    "mild": "5-9",
                    "moderate": "10-14",
                    "moderately_severe": "15-19",
                    "severe": "20-27"
                },
                "clinical_cutoff": 10,
                "interpretation": [
                    "Score ≥10 has 88% sensitivity for major depression",
                    "Item 9 (suicidal ideation) requires immediate clinical attention",
                    "Can track treatment response over time",
                    "2-3 point change is clinically meaningful"
                ]
            },
            "GAD_7": {
                "name": "Generalized Anxiety Disorder-7",
                "purpose": "Anxiety severity screening",
                "scoring": {
                    "range": "0-21",
                    "minimal": "0-4",
                    "mild": "5-9",
                    "moderate": "10-14",
                    "severe": "15-21"
                },
                "clinical_cutoff": 10,
                "interpretation": [
                    "Score ≥10 has 89% sensitivity for GAD",
                    "Also sensitive to panic, social anxiety, PTSD",
                    "Can track treatment response",
                    "2 point change is minimally clinically important"
                ]
            },
            "DIVA_5": {
                "name": "Diagnostic Interview for ADHD in Adults",
                "purpose": "Structured diagnostic interview for ADHD",
                "structure": {
                    "childhood_symptoms": "18 DSM criteria assessed for ages 5-12",
                    "current_symptoms": "18 DSM criteria for current presentation",
                    "examples": "Concrete behavioral examples for each criterion"
                },
                "clinical_note": "Gold standard for ADHD diagnosis; requires trained clinician"
            }
        }

    def get_clinical_red_flags(self) -> Dict[str, List[str]]:
        """Return clinical red flags that require special attention."""
        return {
            "immediate_risk": [
                "Suicidal ideation or plans (PHQ-9 item 9 score > 0)",
                "Self-harm behaviors or intent",
                "Severe functional impairment preventing basic self-care",
                "Psychotic symptoms",
                "Substance abuse with severe impairment"
            ],
            "adhd_misdiagnosis_risk": [
                "No clear childhood history of symptoms",
                "Symptoms only in one context (e.g., only at work)",
                "Recent onset coinciding with mood or life stress",
                "Better explained by anxiety or depression",
                "Adult-onset attention problems without childhood pattern"
            ],
            "depression_misdiagnosis_risk": [
                "Lifelong pattern misattributed to recent depression",
                "Chronic dysthymia mistaken for ADHD-related low mood",
                "Lack of anhedonia or depressed mood",
                "Attention problems present even when mood is good"
            ],
            "requires_specialist_referral": [
                "Bipolar disorder suspected",
                "Complex trauma history",
                "Autism spectrum considerations",
                "Learning disabilities",
                "Substance use disorders",
                "Personality disorder features"
            ]
        }