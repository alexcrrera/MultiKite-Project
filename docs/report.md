# Automatic Take-Off/Landing Strategies and Control for a Multi-Kite Airborne Wind Energy System

## 1. Introduction

### 1.1 Airborne Wind Energy Systems

- Overview of Airborne Wind Energy (AWE).
- Motivation for replacing conventional wind turbines.
- Introduction to the MultiKite concept.
- Industrial constraints and scalability considerations.

### 1.2 Take-Off and Landing Challenge

- Importance of reliable take-off and landing (TOL) procedures.
- Existing desktop prototype and previous work.
- Limitations of the original high-speed spin-up approach.
- Need for a safer and more repeatable solution.

### 1.3 Objectives

The objectives of this project were:

- Develop a controlled take-off and landing strategy.
- Improve repeatability and operational robustness.
- Understand the critical parameters governing successful flight.
- Generate design recommendations for future prototypes.
- Contribute to the development of an automated TOL procedure.

---

# 2. System Description

### 2.1 Multi-Kite System Overview

- General operating principle.
- Flying wings.
- Cross-kite tether arrangement.
- Ground station and rotation mechanism.

### 2.2 Existing Prototype

- Description of the inherited system.
- Observed flight behavior.
- Previously used take-off procedure.

### 2.3 Design Requirements

Requirements identified at the start of the project:

- Repeatable take-off.
- Repeatable landing.
- Safety.
- Ease of testing.
- Compatibility with future automation.

---

# 3. Development of the Take-Off and Landing Structure

### 3.1 Initial Concepts

- Analysis of Version 0.
- Funnel-based guidance concept.
- Wing support philosophy.
- Preliminary experiments.

### 3.2 Mechanical Design

#### 3.2.1 Structural Extensions

- Radial extension.
- Vertical extension.
- Design rationale.

#### 3.2.2 Wing Support Mechanism

- Funnel geometry.
- Contact points.
- Attachment strategy.

#### 3.2.3 Arm Design

Design requirements:

- Low mass.
- High stiffness.
- Limited elongation.
- Ease of manufacturing.

Final design:

- Parametric geometry.
- Lightweight structure.
- Resistance to oscillatory loads.

### 3.3 Electronics and Software Integration

#### User Interface

- Real-time monitoring.
- Quick actions.
- Logging functionality.
- Safety features.

#### System Integration

- Ground station integration.
- Testing workflow.
- Repeatability improvements.

---

# 4. Experimental Methodology

### 4.1 Test Environment

- Test location.
- Experimental setup.
- Operating conditions.

### 4.2 Performance Metrics

Metrics used to evaluate performance:

- Successful take-off.
- Stable flight.
- Successful landing.
- Repeatability.
- Ease of operation.

### 4.3 Experimental Procedure

#### Pre-Flight Preparation

- Wing inspection.
- Mass balancing.
- Tether adjustment.
- Structural verification.

#### Take-Off Procedure

- Wing positioning.
- Initial rotation.
- Progressive reel-out.
- Transition to flight.

#### Landing Procedure

- Controlled reel-in.
- Wing capture.
- System shutdown.

---

# 5. Experimental Results

### 5.1 Iterative Development Process

The system was developed through successive iterations involving:

- Structural modifications.
- Wing balancing.
- Tether length adjustments.
- Attachment point optimization.

### 5.2 Successful Flight Campaign

#### Stable Take-Off

A controlled take-off procedure was successfully demonstrated by:

1. Holding the wings in a predefined configuration.
2. Initiating rotation.
3. Gradually reeling out the tethers.
4. Allowing aerodynamic forces to progressively establish flight.

#### Stable Flight

- Multiple successful flights were achieved.
- Flight was repeatable under the identified configuration.
- Stable rotational behavior was observed.

#### Landing

- Controlled landings were successfully demonstrated.
- The support structure enabled reliable wing capture.

### 5.3 Operational Procedure

A robust operational procedure was established, covering:

- Pre-flight preparation.
- Take-off sequence.
- Flight monitoring.
- Landing sequence.

This procedure significantly improved consistency compared to the previous direct spin-up method.

---

# 6. Sensitivity Analysis and Failure Investigation

### 6.1 Loss of Repeatability

Following a modification of the experimental setup, the previously successful configuration could not be recovered despite extensive measurements and reconstruction efforts.

### 6.2 Critical Parameters Identified

The experiments revealed strong sensitivity to:

- Wing mass distribution.
- Tether lengths.
- Tether attachment positions.
- Wing resting angle.
- Structural alignment.
- Contact conditions within the support structure.
- Small aerodynamic asymmetries.

### 6.3 Observed Failure Modes

Typical failure modes included:

- Failure to lift off.
- Asymmetric take-off.
- Excessive oscillations.
- Premature contact with the structure.
- Unstable flight behavior.

### 6.4 Lessons Learned

A major outcome of this work is the identification of the extreme sensitivity of the take-off phase.

Small variations in geometry or mass distribution can significantly affect system behavior and determine whether take-off succeeds or fails.

This finding highlights the need for:

- Tight manufacturing tolerances.
- Precise assembly procedures.
- Calibration methodologies.
- Improved robustness in future designs.

---

# 7. Discussion

### 7.1 Advantages of the Proposed Approach

Compared to the previous high-speed spin-up method:

- Lower required rotational speeds.
- Improved control during take-off.
- Cleaner landing procedure.
- Better suitability for automation.

### 7.2 Current Limitations

The developed structure presents several drawbacks:

#### Radial Structural Extension

- Increased inertia.
- Increased hazard during operation.

#### Vertical Structural Extension

- Additional mass.
- Increased overall dimensions.

#### General Limitations

- Large footprint.
- Complex assembly.
- Strong parameter sensitivity.

### 7.3 Implications for Future Systems

The results suggest that future designs should prioritize:

- Mechanical simplicity.
- Reduced sensitivity.
- Automated calibration.
- Reduced structural mass.

---

# 8. Next-Generation Take-Off Structure

### 8.1 Motivation

The current structure successfully demonstrated the concept but remains too large and complex for future development.

### 8.2 Proposed Concept

Potential improvements include:

- Retractable support arms.
- Hook-based retention mechanism.
- Passive deployment through centrifugal force.
- Integrated damping mechanisms.

### 8.3 Expected Benefits

Compared to the current version:

- Reduced mass.
- Reduced inertia.
- Smaller storage volume.
- Lower aerodynamic interference.
- Simplified operation.

### 8.4 Future Work

Future efforts should focus on:

- Validation of the new concept.
- Reduction of parameter sensitivity.
- Development of automatic take-off procedures.
- Development of automatic landing procedures.
- Integration with flight control systems.

---

# 9. Conclusion

This project investigated alternative take-off and landing strategies for a MultiKite Airborne Wind Energy system.

A dedicated support structure was designed, constructed, and experimentally validated. Using this structure, repeatable take-off, stable flight, and controlled landing were successfully demonstrated.

The experimental campaign revealed that the system is highly sensitive to small geometric and mass-property variations. While this sensitivity ultimately prevented recovery of the original successful configuration after modifications, it provided valuable insight into the dominant factors governing take-off behavior.

The limitations identified in the current architecture motivated the development of a next-generation concept aimed at reducing mass, inertia, complexity, and sensitivity while improving suitability for future automation.