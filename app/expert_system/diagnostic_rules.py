"""Diagnostic Rules and Clinical Decision Logic.

This module implements rule-based reasoning for differential diagnosis,
incorporating expert clinical judgment patterns.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class DiagnosticEvidence:
    """Evidence supporting or refuting a diagnostic hypothesis."""
    condition: str
    supporting_score: float
    confidence: float
    key_features: List[str]
    contradicting_features: List[str]
    clinical_reasoning: List[str]


class DiagnosticRules:
    """Rule-based diagnostic reasoning system."""
    
    def __init__(self, knowledge_base):
        """Initialize with clinical knowledge base."""
        self.kb = knowledge_base
        
    def evaluate_childhood_onset(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate evidence for childhood onset of symptoms.
        
        Critical for ADHD diagnosis per DSM-5-TR (symptoms before age 12).
        """
        childhood_indicators = [
            responses.get('childhood_school_difficulties', 0),
            responses.get('childhood_attention_problems', 0),
            responses.get('childhood_hyperactivity', 0),
            responses.get('childhood_impulsivity', 0),
            responses.get('parent_teacher_reports_childhood', 0)
        ]
        
        # Calculate evidence strength
        childhood_score = np.mean([x for x in childhood_indicators if x is not None])
        
        # Clinical reasoning
        if childhood_score >= 3.0:  # Assuming 0-4 scale
            evidence_strength = "strong"
            interpretation = "Clear evidence of childhood-onset symptoms consistent with ADHD"
        elif childhood_score >= 2.0:
            evidence_strength = "moderate"
            interpretation = "Some childhood symptoms reported; further detailed history needed"
        else:
            evidence_strength = "weak"
            interpretation = "Limited childhood symptom history; ADHD diagnosis questionable"
        
        return {
            "childhood_onset_score": childhood_score,
            "evidence_strength": evidence_strength,
            "interpretation": interpretation,
            "supports_adhd": childhood_score >= 2.0,
            "clinical_note": "ADHD requires clear evidence of symptoms before age 12 per DSM-5-TR"
        }
    
    def evaluate_symptom_consistency(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate whether symptoms are consistent vs. episodic.
        
        ADHD symptoms are chronic and consistent.
        Depression/anxiety symptoms are often episodic or fluctuating.
        """
        consistency_markers = {
            'lifelong_pattern': responses.get('symptoms_since_childhood', 0),
            'consistent_across_time': responses.get('symptoms_always_present', 0),
            'no_symptom_free_periods': responses.get('no_remission_periods', 0),
            'present_across_contexts': responses.get('symptoms_multiple_settings', 0)
        }
        
        episodic_markers = {
            'recent_onset': responses.get('symptoms_started_recently', 0),
            'clear_episodes': responses.get('distinct_mood_episodes', 0),
            'symptom_free_periods': responses.get('periods_without_symptoms', 0),
            'triggered_by_stress': responses.get('symptoms_worse_with_stress', 0)
        }
        
        consistency_score = np.mean([v for v in consistency_markers.values() if v is not None])
        episodic_score = np.mean([v for v in episodic_markers.values() if v is not None])
        
        if consistency_score > episodic_score + 0.5:
            pattern = "chronic_consistent"
            favors = "ADHD"
        elif episodic_score > consistency_score + 0.5:
            pattern = "episodic_variable"
            favors = "Depression or Anxiety"
        else:
            pattern = "mixed_unclear"
            favors = "Possible comorbidity or requires further assessment"
        
        return {
            "consistency_score": consistency_score,
            "episodic_score": episodic_score,
            "pattern": pattern,
            "favors": favors,
            "clinical_reasoning": [
                "ADHD symptoms are present consistently since childhood",
                "Depression/anxiety tend to have episodic course",
                "Comorbidity shows chronic ADHD with superimposed episodes"
            ]
        }
    
    def evaluate_executive_dysfunction(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate executive function deficits.
        
        Core feature of ADHD; can also occur in depression but pattern differs.
        """
        executive_symptoms = {
            'organization': responses.get('difficulty_organizing_tasks', 0),
            'time_management': responses.get('time_management_problems', 0),
            'planning': responses.get('difficulty_planning_ahead', 0),
            'working_memory': responses.get('forgets_tasks_frequently', 0),
            'task_initiation': responses.get('difficulty_starting_tasks', 0),
            'task_completion': responses.get('does_not_finish_tasks', 0)
        }
        
        ef_score = np.mean([v for v in executive_symptoms.values() if v is not None])
        
        # Assess if EF problems are primary or secondary
        mood_related = responses.get('ef_worse_when_mood_low', 0)
        lifelong_ef = responses.get('ef_problems_since_childhood', 0)
        
        if ef_score >= 3.0 and lifelong_ef >= 3.0:
            interpretation = "Primary executive dysfunction consistent with ADHD"
            pattern = "adhd_primary"
        elif ef_score >= 3.0 and mood_related >= 3.0:
            interpretation = "Executive dysfunction appears secondary to mood disturbance"
            pattern = "depression_secondary"
        elif ef_score >= 3.0:
            interpretation = "Executive dysfunction present; further evaluation of onset needed"
            pattern = "unclear_needs_assessment"
        else:
            interpretation = "Minimal executive dysfunction reported"
            pattern = "low_ef_impairment"
        
        return {
            "ef_score": ef_score,
            "pattern": pattern,
            "interpretation": interpretation,
            "supports_adhd": pattern == "adhd_primary",
            "clinical_note": "Executive dysfunction in ADHD is lifelong; in depression it's episodic"
        }
    
    def evaluate_mood_symptoms(self, phq9_score: int, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate depressive symptoms and their relationship to other symptoms."""
        
        # Core mood symptoms
        anhedonia = responses.get('little_interest_or_pleasure', 0)
        depressed_mood = responses.get('feeling_down_depressed_hopeless', 0)
        
        # Severity classification
        if phq9_score >= 15:
            severity = "moderately_severe_to_severe"
            clinical_significance = "high"
        elif phq9_score >= 10:
            severity = "moderate"
            clinical_significance = "moderate"
        elif phq9_score >= 5:
            severity = "mild"
            clinical_significance = "low_to_moderate"
        else:
            severity = "minimal"
            clinical_significance = "minimal"
        
        # Assess relationship to attention problems
        attention_improves_mood_good = responses.get('attention_better_when_mood_good', 0)
        episodic_pattern = responses.get('mood_episodes_clear_onset', 0)
        
        if phq9_score >= 10 and episodic_pattern >= 3:
            primary_condition = "depression"
            reasoning = "Significant depressive symptoms with episodic pattern"
        elif phq9_score >= 10 and attention_improves_mood_good >= 3:
            primary_condition = "depression_with_secondary_attention_problems"
            reasoning = "Depression causing secondary cognitive symptoms"
        elif phq9_score >= 5 and phq9_score < 10:
            primary_condition = "mild_depression_or_secondary_to_adhd"
            reasoning = "Mild mood symptoms; could be secondary to chronic ADHD impairment"
        else:
            primary_condition = "minimal_depression"
            reasoning = "Depression not a primary concern"
        
        return {
            "phq9_score": phq9_score,
            "severity": severity,
            "clinical_significance": clinical_significance,
            "primary_condition": primary_condition,
            "reasoning": reasoning,
            "requires_treatment": phq9_score >= 10,
            "suicidal_risk": responses.get('thoughts_better_off_dead', 0) > 0
        }
    
    def evaluate_anxiety_symptoms(self, gad7_score: int, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate anxiety symptoms and their relationship to other symptoms."""
        
        # Core anxiety symptoms
        excessive_worry = responses.get('feeling_nervous_anxious_on_edge', 0)
        difficulty_controlling_worry = responses.get('not_able_to_stop_or_control_worrying', 0)
        
        # Severity classification
        if gad7_score >= 15:
            severity = "severe"
            clinical_significance = "high"
        elif gad7_score >= 10:
            severity = "moderate"
            clinical_significance = "moderate"
        elif gad7_score >= 5:
            severity = "mild"
            clinical_significance = "low_to_moderate"
        else:
            severity = "minimal"
            clinical_significance = "minimal"
        
        # Assess relationship to attention problems
        attention_due_to_worry = responses.get('distraction_due_to_worry', 0)
        restlessness_type = responses.get('restlessness_tense_vs_driven', 0)  # 1=tense, 2=driven
        
        if gad7_score >= 10 and attention_due_to_worry >= 3:
            primary_condition = "anxiety_with_worry_based_distraction"
            reasoning = "Anxiety causing attention problems via worry and preoccupation"
        elif gad7_score >= 10 and restlessness_type == 1:
            primary_condition = "anxiety_primary"
            reasoning = "Anxiety with tense restlessness (not ADHD-driven restlessness)"
        elif gad7_score >= 5 and gad7_score < 10:
            primary_condition = "mild_anxiety_or_secondary_to_adhd"
            reasoning = "Mild anxiety; could be secondary to chronic ADHD-related failures"
        else:
            primary_condition = "minimal_anxiety"
            reasoning = "Anxiety not a primary concern"
        
        return {
            "gad7_score": gad7_score,
            "severity": severity,
            "clinical_significance": clinical_significance,
            "primary_condition": primary_condition,
            "reasoning": reasoning,
            "requires_treatment": gad7_score >= 10
        }
    
    def apply_differential_rules(self, 
                                adhd_score: float,
                                phq9_score: int,
                                gad7_score: int,
                                childhood_data: Dict,
                                consistency_data: Dict,
                                ef_data: Dict) -> List[DiagnosticEvidence]:
        """Apply differential diagnostic rules to generate diagnostic hypotheses."""
        
        evidence_list = []
        
        # ADHD Hypothesis
        adhd_supporting = []
        adhd_contradicting = []
        adhd_reasoning = []
        
        # Strong childhood onset evidence
        if childhood_data['supports_adhd']:
            adhd_supporting.append("Clear childhood symptom onset before age 12")
            adhd_reasoning.append("DSM-5-TR requires symptom onset before age 12 for ADHD")
        else:
            adhd_contradicting.append("Weak or absent childhood symptom history")
            adhd_reasoning.append("No clear childhood onset argues against ADHD diagnosis")
        
        # Chronic consistent pattern
        if consistency_data['pattern'] == 'chronic_consistent':
            adhd_supporting.append("Chronic, consistent symptom pattern")
            adhd_reasoning.append("ADHD symptoms are lifelong and consistent, not episodic")
        
        # Primary executive dysfunction
        if ef_data['pattern'] == 'adhd_primary':
            adhd_supporting.append("Primary executive dysfunction since childhood")
            adhd_reasoning.append("Core ADHD feature is primary executive dysfunction")
        
        # Low mood/anxiety scores favor ADHD alone
        if phq9_score < 10 and gad7_score < 10:
            adhd_supporting.append("Minimal depression and anxiety symptoms")
        elif phq9_score >= 10 or gad7_score >= 10:
            adhd_supporting.append("Comorbid mood/anxiety symptoms present")
            adhd_reasoning.append("30-50% of ADHD adults have comorbid depression or anxiety")
        
        # Calculate ADHD confidence
        adhd_confidence = 0.0
        if childhood_data['supports_adhd']:
            adhd_confidence += 0.4
        if consistency_data['pattern'] == 'chronic_consistent':
            adhd_confidence += 0.3
        if ef_data['supports_adhd']:
            adhd_confidence += 0.3
        
        # Normalize by ADHD score
        adhd_final_score = (adhd_score / 72.0) * adhd_confidence  # ASRS max is 72
        
        evidence_list.append(DiagnosticEvidence(
            condition="ADHD",
            supporting_score=adhd_final_score,
            confidence=adhd_confidence,
            key_features=adhd_supporting,
            contradicting_features=adhd_contradicting,
            clinical_reasoning=adhd_reasoning
        ))
        
        # Depression Hypothesis
        depression_supporting = []
        depression_contradicting = []
        depression_reasoning = []
        
        if phq9_score >= 10:
            depression_supporting.append(f"PHQ-9 score of {phq9_score} indicates moderate or greater depression")
            depression_reasoning.append("PHQ-9 ≥10 has 88% sensitivity for major depression")
        
        if consistency_data['pattern'] == 'episodic_variable':
            depression_supporting.append("Episodic symptom pattern")
            depression_reasoning.append("Depression typically has episodic course with remissions")
        
        if ef_data['pattern'] == 'depression_secondary':
            depression_supporting.append("Cognitive symptoms appear secondary to mood")
            depression_reasoning.append("Depression causes secondary attention and concentration problems")
        
        if not childhood_data['supports_adhd'] and phq9_score >= 10:
            depression_reasoning.append("Lack of childhood symptoms argues against ADHD; depression more likely")
        
        depression_confidence = min(1.0, (phq9_score / 27.0) * 1.5)
        
        evidence_list.append(DiagnosticEvidence(
            condition="Major Depressive Disorder",
            supporting_score=phq9_score / 27.0,
            confidence=depression_confidence,
            key_features=depression_supporting,
            contradicting_features=depression_contradicting,
            clinical_reasoning=depression_reasoning
        ))
        
        # Anxiety Hypothesis
        anxiety_supporting = []
        anxiety_contradicting = []
        anxiety_reasoning = []
        
        if gad7_score >= 10:
            anxiety_supporting.append(f"GAD-7 score of {gad7_score} indicates moderate or greater anxiety")
            anxiety_reasoning.append("GAD-7 ≥10 has 89% sensitivity for anxiety disorders")
        
        anxiety_confidence = min(1.0, (gad7_score / 21.0) * 1.5)
        
        evidence_list.append(DiagnosticEvidence(
            condition="Generalized Anxiety Disorder",
            supporting_score=gad7_score / 21.0,
            confidence=anxiety_confidence,
            key_features=anxiety_supporting,
            contradicting_features=anxiety_contradicting,
            clinical_reasoning=anxiety_reasoning
        ))
        
        return evidence_list
    
    def generate_primary_diagnosis(self, evidence_list: List[DiagnosticEvidence]) -> Dict[str, Any]:
        """Generate primary diagnostic conclusion based on evidence."""
        
        # Sort by weighted score (supporting_score * confidence)
        weighted_scores = [
            (ev.condition, ev.supporting_score * ev.confidence, ev)
            for ev in evidence_list
        ]
        weighted_scores.sort(key=lambda x: x[1], reverse=True)
        
        primary = weighted_scores[0]
        
        # Check for comorbidity
        comorbid_conditions = []
        for cond, score, ev in weighted_scores[1:]:
            if score >= 0.3:  # Threshold for clinical significance
                comorbid_conditions.append(cond)
        
        # Generate conclusion
        if len(comorbid_conditions) == 0:
            diagnostic_impression = f"Primary pattern consistent with {primary[0]}"
            complexity = "single_condition"
        elif len(comorbid_conditions) == 1:
            diagnostic_impression = f"Primary pattern: {primary[0]} with comorbid {comorbid_conditions[0]}"
            complexity = "comorbid_two_conditions"
        else:
            diagnostic_impression = f"Complex presentation: {primary[0]} with multiple comorbid conditions"
            complexity = "complex_multiple_conditions"
        
        return {
            "primary_condition": primary[0],
            "primary_score": primary[1],
            "comorbid_conditions": comorbid_conditions,
            "diagnostic_impression": diagnostic_impression,
            "complexity": complexity,
            "all_evidence": weighted_scores,
            "clinical_recommendation": self._generate_recommendation(primary[0], comorbid_conditions, complexity)
        }
    
    def _generate_recommendation(self, primary: str, comorbid: List[str], complexity: str) -> List[str]:
        """Generate clinical recommendations based on findings."""
        recommendations = []
        
        recommendations.append("⚕️ This is a SCREENING TOOL ONLY - not a diagnosis")
        recommendations.append("Formal evaluation by a qualified mental health professional is necessary")
        
        if primary == "ADHD":
            recommendations.append("Comprehensive ADHD evaluation should include:")
            recommendations.append("  - Detailed childhood and developmental history")
            recommendations.append("  - Collateral information from family members")
            recommendations.append("  - Assessment of functional impairment across settings")
            recommendations.append("  - Ruling out other conditions (mood, anxiety, learning disabilities)")
            
        if "Major Depressive Disorder" in [primary] + comorbid:
            recommendations.append("Depression screening positive - evaluation should address:")
            recommendations.append("  - Suicide risk assessment")
            recommendations.append("  - Duration and severity of current episode")
            recommendations.append("  - History of previous episodes")
            recommendations.append("  - Consideration of psychotherapy and/or medication")
            
        if "Generalized Anxiety Disorder" in [primary] + comorbid:
            recommendations.append("Anxiety screening positive - evaluation should include:")
            recommendations.append("  - Specific anxiety disorder subtype assessment")
            recommendations.append("  - Impact on daily functioning")
            recommendations.append("  - Consideration of CBT and/or medication")
            
        if complexity in ["comorbid_two_conditions", "complex_multiple_conditions"]:
            recommendations.append("⚠️ Complex presentation with multiple conditions:")
            recommendations.append("  - Integrated treatment approach needed")
            recommendations.append("  - Consider psychiatrist referral for medication management")
            recommendations.append("  - Psychotherapy for comorbid conditions")
            
        return recommendations