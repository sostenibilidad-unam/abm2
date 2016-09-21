
extensions [stats profiler matrix]
globals [              ;;DEFINE GLOBAL VARIABLES
  real_rain            ;; real annual rainfall
  R                    ;; climatic risk (rainfall transformed into a normalized [0-1] scale)
  rain_max_obs         ;;max rainfall observed

  Prob_H_F             ;;probability of hazarous event floooding
  Prob_H_S             ;;probability of hazarous event scarcity

;##################################
;;;;;;weights of criterions for goverment decisions
;##################################
  matrix_A
  matrix_B
  w_11_demanda_F                    ;;Economic efficiency criteria
  w_12_presion_F                    ;;Social response criteria
  w_13_estado_F                    ;;Infrastructure criteria

  w_21_necesidad_F                   ;;Economic efficiency criteria
  w_22_presion_F                    ;;Social response criteria
  w_23_estado_F                    ;;Infrastructure criteria


  w_31_demanda_S                    ;;Economic efficiency criteria
  w_32_presion_S                    ;;Social response criteria
  w_33_estado_S                    ;;Infrastructure criteria

  w_41_necesidad_S                    ;;Economic efficiency criteria
  w_42_presion_S                    ;;Social response criteria
  w_43_estado_S                    ;;Infrastructure criteria



  C11max                  ;;max efficiency recorded
  C12max                  ;;max protests recorded
  C13max                  ;;max age infra recorded

  C21max                  ;;max efficiency recorded
  C22max                  ;;max protests recorded
  C23max                  ;;max age infra recorded

  C31max                  ;;max efficiency recorded
  C32max                  ;;max protests recorded
  C33max                  ;;max age infra recorded

  C41max                  ;;max efficiency recorded
  C42max                  ;;max protests recorded
  C43max                  ;;max age infra recorded



;##################################
;;Reporters
;##################################
  Var_list             ;;To report vulnerability at the final 100
  max_damage           ;;max damage in the city. It helps to calculate the tolerance threshold tau in the vulnerability procedure by comparing the state of the agents with respect to to waalth {W] and the average damage (mean_damage)

  lorenz-points_V      ;;variable to calculate lorenz curve for innequality (need to think what does it mean)
  gini_V               ;;gini coefitient of the vulnerability

  max_v                ;;auxiliar variable to calculate neighborhood with the maximal level of vulnerability
  counter              ;;count in a for-loop
  max_protest_F          ;;maximum number of protest recorded in a year
  max_protest_S
  ExposureIndex        ; average of the double exposure during last 100 ticks

  EfficiencyIndex      ;average number of events a person suffer in the city
  EfficiencyIndex_S    ;average level of scarcity of a person in the city
  EfficiencyIndex_F    ;average number of flooding a person suffer in the city

  InequalityExposureIndex ; distribution of exposure to both events

  StateinfraIndex_S    ;report the number of patches with functioning infrastructure
  StateinfraIndex_F    ;report the number of patches with functioning infrastructure
  StateinfraAgeIndex_S ;report the mean age of infrastructure S
  StateinfraAgeIndex_F ;report the mean age of infrastructure F

  socialpressureIndex_S ;report the sum of protest in the city
  socialpressureIndex_F ;report the sum of protest in the city

  socialpressureTOTALIndex_S ;report the sum of protest in the city
  socialpressureTOTALIndex_F ;report the sum of protest in the city
]




;######################################################################
;define patches and patch variables
;Patches can be seen as the minimal geostatitical unit at which goverment collect information to decide where to invest.
;######################################################################
patches-own[

  district_here?            ;;ture if the patch contains a district there
  Infra_flood               ;;IS= 1 If the patch has an infrastructure piece; IS = 0 if not
  Infra_supply              ;;IS= 1 If the patch has an infrastructure piece; IS = 0 if not

  P_failure_F               ;;Probability of failure of infrastructure-here (P_failure =1 if not infra here; P_failure =0 if infrastructure is new)
  P_failure_S               ;;Probability of failure of infrastructure-here (P_failure =1 if not infra here; P_failure =0 if infrastructure is new)
  infra_F_age               ;;age infrastructure Flooding
  infra_S_age               ;;age infrastructure supply

  A                         ;;Altitute


  C11-Efficiencia           ;;criteria use to measure # people benefitiated if investment is made
  C12-Social_pressure       ;;criteria use by gov to measure social pressure due to flooding
  C13-InfraState            ;;variable that messure the age of infra in each patch with IS >0

  C21-need                  ;;criteria to messure the need for infra based on # people without infrastructure
  C22-Social_pressure       ;;criteria use by gov to measure social pressure due to flooding
  C23-InfraState

  C31-Efficiencia
  C32-Social_pressure       ;;criteria use by gov to measure social pressure due to scarcity
  C33-InfraState

  C41-need                  ;;criteria to messure the need for infra based on # people without infrastructure
  C42-Social_pressure       ;;criteria use by gov to measure social pressure due to scarcity
  C43-InfraState



  distance_metric_maintenance_A1   ;;Metric for define distance from ideal point (MDCA)
  distance_metric_New_A2           ;;Metric for define distance from ideal point (MDCA)
  distance_metric_maintenance_A3   ;;Metric for define distance from ideal point (MDCA)
  distance_metric_New_A4           ;;Metric for define distance from ideal point (MDCA)

  protestas_here_F            ;;Social pressure (protests) accumulated over time in a neighborhood due to flooding
  protestas_here_S            ;;Social pressure (protests) accumulated over time in a neighborhood due to scarcity



  H_F                       ;;1 if a hazard event occur 0 otherwise
  H_S                       ;;1 if a hazard event occur 0 otherwise
  V                         ;; Vulnerability==Sensitivity * EE
  exposure_F                ;; exposure to harmful events (F Flooding or S scarcity). It is a "moving average" of events occuring over time
  exposure_S
  total_exposure_F
  total_exposure_S
]

;#############################################################################################

;######################################################################
;######################################################################
to create_landscape
  random-seed semilla-aleatoria
  if landscape-type = "closed watershed"[
  ask patches with [(pxcor =  50 and pycor = 50)][set A 5000] ;;define central point with max value.

  repeat 300 [diffuse A  1]   ;; slightly smooth out the landscape by difusing variables A (this can be modified to include other topography with other method or using real data.
  ]

  if landscape-type = "many hills"[
    ask n-of 10 patches [set A (4500 + random 500)] ;;define central point with max value.
  repeat 100 [diffuse A  1]
  ]


  let max_alt max [A] of patches   ;;define maximum altitute
  let min_alt min [A] of patches   ;;define minimum altitute
  ask patches [
    if landscape-type = "closed watershed" [
      set A (max_alt - A) / max_alt
    ]

    if landscape-type = "many hills" [
      set A A / max_alt
    ]

    if landscape-type = "gradient"[
      set A (max-pxcor - pxcor) / max-pxcor          ;;define topographic risk as a gradient with respect to pxcor
    ]


    set Infra_flood 0
    set Infra_supply 0

    set P_failure_F 1
    set P_failure_S 1

    set infra_F_age 0
    set infra_S_age 0

    set protestas_here_F  0
    set protestas_here_S  0
    set total_exposure_S 0
    set total_exposure_F 0

    set district_here? FALSE

    set C11-Efficiencia 0.01
    set C12-Social_pressure 0.001
    set C13-InfraState infra_F_age

    set C21-need 0.1
    set C22-Social_pressure 0.001
    set C23-InfraState infra_F_age

    set C31-Efficiencia 0.01;Criteria 1 economic efficiancy. calcuate number of neighborhoods beneficiated per "dolar" invested
    set C32-Social_pressure 0.001                   ;;criteria 2. collect the number of protest in the district located in this patch
    set C33-InfraState infra_S_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch

    set C41-need 0.1
    set C42-Social_pressure  0.001                   ;;criteria 2. collect the number of protest in the district located in this patch
    set C43-InfraState infra_S_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch

    set pcolor 65
  ]


end

;#############################################################################################
to Create-Districts-Infra

  ask patches [

    if A < random-float 1 [
      set district_here? TRUE
      set   protestas_here_F  0.1
      set   protestas_here_S  0.1
      if A < random-float 1 [
        set Infra_flood 1              ;; 1 if infra for "drainage" is here; 0 otherwise
        set infra_F_age 1
        set P_failure_F 1 - exp(- infra_F_age / 100)
      ]
      if A < random-float 1 [
        set Infra_supply 1
        set infra_S_age 1             ;; 1 if infra for "water supply" is here; 0 otherwise
        set P_failure_S 1 - exp(- infra_S_age / 100)
      ]
    ]


    set V exposure_F + exposure_S                                           ;; Vulnerability






  ]

end


;#####################################################################
;#####################################################################
;SETUP
;#####################################################################
;#####################################################################

to setup

  clear-all ;;clean plots and global variables

;;set global
  set Var_list []
  set lorenz-points_V []
  create_landscape         ;;define landscape topography (Altitute)
  Create-Districts-Infra       ;;define the properties of the infrastructure and the neighborhoods
  read_weightsfrom_matrix

  set ExposureIndex 0
  set EfficiencyIndex 0
  set EfficiencyIndex_S 0
  set EfficiencyIndex_F 0
  set StateinfraIndex_S 0
  set StateinfraIndex_F 0
  set InequalityExposureIndex 0
  set socialpressureIndex_S 0
  set socialpressureIndex_F 0
  set rain_max_obs (max_rain_recorded p_rain) ;;set max rainfall observed

  reset-ticks
end


;#################################################################################
;#################################################################################
;;GO
;#################################################################################
;#################################################################################

to GO
  ;profiler:start  ;;to check the computational time needed per procedude
  tick

  update_globals_and_reporters ;; to update global and reporters
  rain                   ;;set the magnitude of the climatic event and the risk factor
  ask patches [
    collect_information
    Hazard                 ;; To define if a neighborhood suffer a hazard (H=1), or not (H=0), in a year
    vulnerability
    protest
    Landscape_visualization
  ]

  WGA_decisions ;; Water government authority decides in what (new vs. maitainance flooding vs. scarcity) and where (in what districts) to invest resources (budget)
  update_state_infrastructure ;update state of infrastructure (age, prob. of failure)

if ticks = 600 [update_weights]
if ticks = 499 [export_view]

if ticks = 500 [stop]
 ; profiler:stop          ;; stop profiling
 ; print profiler:report  ;; view the results
 ; profiler:reset         ;; clear the data
end


;###############################################################################
to rain   ;;GENERATE CLIMATIC REALIZATIONS USING A NORMAL DISTRICUTION AND CONVERTED TO A RISK CLIMATIC FACTOR BY NORMALIZING THE SCALE
  set real_rain log-normal 1 p_rain              ;;generate a normal realization
  if (real_rain > rain_max_obs) [set rain_max_obs real_rain]   ;;to update max observation if greater than 200
  set R real_rain / rain_max_obs                               ;;convert to a risk scale between 0 and 1.
end


;###############################################################################
to Hazard                                                                                                           ;;GENERATE HAZARDOUS EVENTS IN EACH PATCH OCCUPID BY A DISTRICT
    if district_here? = TRUE [
      let IS_N (sum [P_failure_F] of patches in-radius 2 + P_failure_F) / (1 + count patches in-radius 2)           ;;update the average state of infrastructure in patches in radius 2
      let IS_S (sum [P_failure_S] of patches in-radius 2 + P_failure_S) / (1 + count patches in-radius 2)           ;;update the average state of infrastructure in patches in radius 2

      set Prob_H_F IS_N  * R * (1 - A)                                                                                    ;;update probability of hazardous event
      set H_F ifelse-value (Prob_H_F >= random-float 1) [1][0]                                                      ;;update hazard counter to 1
      set exposure_F precision (0.9 * exposure_F + H_F) 3                                                           ;;update memory of past events
      if ticks > 400[
        set total_exposure_F total_exposure_F + H_F
      ]
      set Prob_H_S IS_S * A
      set H_S Prob_H_S                                                                                              ;;update hazard counter to 1
      set exposure_S precision (0.9 * exposure_S + H_S) 3
      if ticks > 400[                                                          ;;update list (memory) of past events
        set total_exposure_S total_exposure_S + H_S
      ]
    ]
end


;###############################################################################
to Landscape_visualization                                                                                                             ;;TO REPRESENT DIFFERENT INFORMATION IN THE LANDSCAPE
  if Visualization = "Infrastructure_F" [set pcolor ifelse-value (Infra_flood = 1)[scale-color grey  (1 - P_failure_F) 0  1][65]]      ;;probability of Infrastructure failure
  if Visualization = "Infrastructure_S" [set pcolor ifelse-value (Infra_supply = 1)[scale-color grey  (1 - P_failure_S) 0  1][65]]     ;;probability of Infrastructure failure
  if Visualization = "Vulnerability" [set pcolor ifelse-value (District_here? = TRUE) [scale-color blue V 0 max_v][65]]                ;;visualize vulnerability
  if visualization = "Social Pressure_F" [set pcolor ifelse-value (District_here? = TRUE) [scale-color red   protestas_here_F  0 10][black]];;visualized social pressure
  if visualization = "Social Pressure_S" [set pcolor ifelse-value (District_here? = TRUE) [scale-color red   protestas_here_S  0 10][black]];;visualized social pressure
  if visualization ="Spatial priorities maintanance F" [set pcolor scale-color magenta  distance_metric_maintenance_A1 0 1]              ;;priorities
  if visualization ="Spatial priorities maintanance S" [set pcolor scale-color sky  distance_metric_maintenance_A3 0 1]              ;;priorities

  if visualization ="Spatial priorities new F" [set pcolor scale-color magenta distance_metric_New_A2 0 1]                               ;;priorities
  if visualization ="Spatial priorities new S" [set pcolor scale-color sky distance_metric_New_A4 0 1]                               ;;priorities

  if visualization = "Districts" [set pcolor ifelse-value (District_here? = TRUE) [magenta][65]]                                       ;;visualize if neighborhood are present in the landscape (green color if not)
  if visualization ="Harmful Events" [                                                                                                 ;; here the harmful events red color when both events( flloding and scarcity occur)
    ifelse district_here? = false [set pcolor 65]
    [
     set pcolor H_S * 35 + H_F * 85 - 105 * (H_F * H_S)
    ]
  ]
end


;###############################################################################
to vulnerability;;PROCEDURE TO COMPUTE VULNERABILITY INDICE
  set V precision (exposure_F + exposure_S) 3                                   ;;calculate vulnerability as the product of exposure
end


;###############################################################################
to protest ;;AN STOCHASTIC PROCESS THAT SIMUALTE A PROTEST RANDOMLY BUT PROPROTIONALY TO TIME ALLOCATED TO PROTESTING
  let prot_F ifelse-value ((exposure_F / 10) > random-float 1)[1][0]
  let prot_S ifelse-value ((exposure_S / 10) > random-float 1)[1][0]

  set   protestas_here_F  0.9 * protestas_here_F + prot_F                                        ;;update patch variable to be collected by the government
  set   protestas_here_S  0.9 * protestas_here_S + prot_S                                       ;;update patch variable to be collected by the government

if ticks > 400 [
  set   socialpressureTOTALIndex_S socialpressureTOTALIndex_S + prot_F
  set   socialpressureTOTALIndex_F socialpressureTOTALIndex_F + prot_S
]
end


;###############################################################################
to collect_information    ;; GOVERNMENT SURVEILLANCE SYSTEM
 set C11-Efficiencia ((count patches in-radius 2 with [district_here? = TRUE]) + (ifelse-value (district_here? = TRUE)[1][0])) ;* (ifelse-value (any? patches in-radius 2 with [Infra_flood = 1] or Infra_flood = 1)[(P_failure_F + sum [P_failure_F] of patches in-radius 2 with [Infra_flood = 1])/(1 + count patches in-radius 2 with [Infra_flood = 1])][1])  ;Criteria 1 economic efficiancy. calcuate number of neighborhoods beneficiated per "dolar" invested
 set C12-Social_pressure   protestas_here_F                   ;;criteria 2. collect the number of protest in the district located in this patch
 set C13-InfraState infra_F_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch

 set C21-need ((count patches in-radius 2 with [Infra_flood = 0]) + (1 - Infra_flood)) * ((ifelse-value (district_here? = TRUE)[1][0]) + (count patches in-radius 2 with [district_here? = TRUE]))
 set C22-Social_pressure protestas_here_F                   ;;criteria 2. collect the number of protest in the district located in this patch
 set C23-InfraState infra_F_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch

 set C31-Efficiencia (count patches in-radius 2 with [district_here? = TRUE] + (ifelse-value (district_here? = TRUE)[1][0])) ;*    (ifelse-value (any? patches in-radius 2 with [Infra_supply = 1] or Infra_supply = 1)[(P_failure_S + sum [P_failure_S] of patches in-radius 2 with [Infra_supply = 1])/(1 + count patches in-radius 2 with [Infra_supply = 1])][1])  ;Criteria 1 economic efficiancy. calcuate number of neighborhoods beneficiated per "dolar" invested
 set C32-Social_pressure protestas_here_S                   ;;criteria 2. collect the number of protest in the district located in this patch
 set C33-InfraState infra_S_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch

 set C41-need (count patches in-radius 2 with [Infra_supply = 0] +  (1 - Infra_supply)) * ((ifelse-value (district_here? = TRUE)[1][0]) + (count patches in-radius 2 with [district_here? = TRUE]))
 set C42-Social_pressure   protestas_here_S                   ;;criteria 2. collect the number of protest in the district located in this patch
 set C43-InfraState infra_S_age  ;;criteria 3. Collect information about the age of the infrastructure in the current patch
end

;;####################################################################################
;;Water government authority define priorities based on the prioritization strategy
;;####################################################################################
to WGA_decisions
;   ; if GOVERNMENT_DECISION_MAKING = "Social Benefit"[                 ;;C1: priority for economic efficiency (increase benefits to people (less $ per people)
;   ;   set w_11 0.8
;      set w_12 0.1
;      set w_13 0.1
;
;      set w_21 0.8
;      set w_22 0.1
;      set w_23 0.1
;
;      set w_31 0.8
;      set w_32 0.1
;      set w_33 0.1
;
;      set w_41 0.8
;      set w_42 0.1
;      set w_43 0.1
;    ]
;    if GOVERNMENT_DECISION_MAKING = "Response to Social Pressure"[         ;;C2: priority for Social efficiency (intevine to reduce number of protests)
;      set w_11 0.1
;      set w_12 0.8
;      set w_13 0.1
;
;      set w_21 0.1
;      set w_22 0.8
;      set w_23 0.1
;
;      set w_31 0.1
;      set w_32 0.8
;      set w_33 0.1
;
;
;      set w_41 0.1
;      set w_42 0.8
;      set w_43 0.1
;
;    ]
;    if GOVERNMENT_DECISION_MAKING = "State of infrastructure"[                ;;C3: priority for engeniering efficiency (reduce damage_F by intervine aged of infrastructure)
;      set w_11 0.1
;      set w_12 0.1
;      set w_13 0.8
;
;      set w_21 0.1
;      set w_22 0.1
;      set w_23 0.8
;
;      set w_31 0.1
;      set w_32 0.1
;      set w_33 0.8
;
;      set w_41 0.1
;      set w_42 0.1
;      set w_43 0.8
;
;    ]



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;goverment select patches according to a distance metric and Compromised programing optimiation

;;1) obtain information from the state of the coupled human-infrastucture system (procedure "collect_information")
;;2) tranform the information to an standarized scale using "value functions"
;;3) calculate a distance metric between the state of each patch, based on the criterion, and the ideal point.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ask patches [
      ;C11 people affected positIvely if WGA repare or maintain dranage infrastructure
      ;C12 Average amount of social pressure in each patch
      ;C13 Age infrastructure


       let Vf_11 ifelse-value (C11-Efficiencia < C11max)[(C11-Efficiencia / C11max)][1]                                                                             ;;define the value functions by transforming natural scale of the information gethered by goverment
       let Vf_12 ifelse-value (C12-Social_pressure < C12max)[(C12-Social_pressure / C12max)][1]                                                                     ;;to a standarized scale [0,1] where 1 means maximal atention from goverment (1 = larger number of protested in an area

       let Vf_13 0
       set Vf_13 ifelse-value (C13-InfraState < 50)[C13-InfraState / 50] [(C13max - C13-InfraState) / 50]
       if C13-InfraState > 100 or C13-InfraState = 0[set Vf_13 0]


       let Vf_21 ifelse-value (C21-need < C21max)[C21-need / C21max][1]
       let Vf_22 ifelse-value (C22-Social_pressure <= C22max)[C22-Social_pressure / C22max][1]

       let Vf_23 ifelse-value (C23-InfraState < 50)[0][2 * (C23-InfraState - 50) / C23max]
       if C23-InfraState > 100 or C23-InfraState = 0 [set Vf_23 1]

       let Vf_31 ifelse-value (C31-Efficiencia < C31max)[(C31-Efficiencia / C31max)][1]                                                                             ;;define the value functions by transforming natural scale of the information gethered by goverment
       let Vf_32 ifelse-value (C32-Social_pressure < C32max)[(C32-Social_pressure / C32max)][1]                                                                     ;;to a standarized scale [0,1] where 1 means maximal atention from goverment (1 = larger number of protested in an area
       let Vf_33 ifelse-value (C33-InfraState < 50)[C33-InfraState / 50] [(C33max - C33-InfraState) / 50]
       if C33-InfraState > 100 or C33-InfraState = 0 [set Vf_33 0]


       let Vf_41 ifelse-value (C41-need <= C41max)[C41-need / C41max][1]
       let Vf_42 ifelse-value (C42-Social_pressure <= C42max)[C42-Social_pressure / C42max][1]
       let Vf_43 ifelse-value (C43-InfraState <= 50)[0][2 * (C43-InfraState - 50) / C43max]
       if C43-InfraState > 100 or C43-InfraState = 0 [set Vf_43 1]



       let h_Cp 1
       set distance_metric_maintenance_A1 precision (((w_11_demanda_F ^ h_Cp) * (Vf_11 ^ h_Cp) + (w_12_presion_F ^ h_Cp) * (Vf_12 ^ h_Cp) + (w_13_estado_F ^ h_Cp)  * (Vf_13 ^ h_Cp)) ^ (1 / h_Cp)) 3              ;calcualte distance to ideal point
       set distance_metric_New_A2 precision (((w_21_necesidad_F ^ h_Cp) * (Vf_21 ^ h_Cp) + (w_22_presion_F ^ h_Cp) * (Vf_22 ^ h_Cp) + (w_23_estado_F ^ h_Cp)  * (Vf_23 ^ h_Cp)) ^ (1 / h_Cp)) 3

       set distance_metric_maintenance_A3 precision (((w_31_demanda_S ^ h_Cp) * (Vf_31 ^ h_Cp) + (w_32_presion_S ^ h_Cp) * (Vf_32 ^ h_Cp) + (w_33_estado_S ^ h_Cp)  * (Vf_33 ^ h_Cp)) ^ (1 / h_Cp)) 3              ;calcualte distance to ideal point
       set distance_metric_New_A4 precision (((w_41_necesidad_S ^ h_Cp) * (Vf_41 ^ h_Cp) + (w_42_presion_S ^ h_Cp) * (Vf_42 ^ h_Cp) + (w_43_estado_S ^ h_Cp)  * (Vf_43 ^ h_Cp)) ^ (1 / h_Cp)) 3

    ]


     let tot_cost_Maintance 0
     let bud_mant (count patches with [district_here? = true]) * maintenance / 1350
      let rank_A1 sort-on [1 - distance_metric_maintenance_A1] patches                                             ;;;sort neighborhoods based on distance metric Action 1 mantanance F.
      let rank_A3 sort-on [1 - distance_metric_maintenance_A3] patches                                             ;;;sort neighborhoods based on distance metric Action 3 mantanance S.

       (foreach rank_A1 rank_A3 [
         if [infra_flood] of ?1 = 1 [
           ask ?1 [
             if distance_metric_maintenance_A1 > random-float 1 and tot_cost_Maintance < bud_mant[                 ;;if total cost until now is lower than budget then mantain the infra in this patch
               set tot_cost_Maintance tot_cost_Maintance + 1                                                          ;;add to the total cost
               set infra_F_age infra_F_age - 0.4 * infra_F_age                                                        ;;update the state (age) of infrastructure
             ]
           ]
         ]

         if [infra_supply] of ?2 = 1[
          ask ?2 [
             if distance_metric_maintenance_A3 > random-float 1 and tot_cost_Maintance <  bud_mant[                  ;; Water autority would repare if the distance is alrge than a random number betwee 0 and 1 and if total cost upto this point is lower than budget
               set tot_cost_Maintance tot_cost_Maintance + 1                                                           ;;add new cost to total cost
               set infra_S_age infra_S_age - 0.4 * infra_S_age                                                         ;;update the state (age) of infrastructure
             ]
           ]
         ]
       ])

       if ticks mod 10 = 0[                                                                                            ;;in years when government invest in new infrastructure
         let tot_cost_New 0
         let bud_new (count patches with [district_here? = true]) * New_infra_investment / 1350
         let rank_A2 sort-on [1 - distance_metric_New_A2] patches                                                      ;;;sort neighborhoods based on distance metric Action 3 new infra F.
         let rank_A4 sort-on [1 - distance_metric_New_A4] patches                                                      ;;;sort neighborhoods based on distance metric Action 4 new infra F.
         (foreach  rank_A2  rank_A4[

           ask ?1 [
             if distance_metric_New_A2 > random-float 1 and tot_cost_New < bud_new[                                                                  ;;if total cost until now is lower than budget for new investments, then create new infra in this patch
               set tot_cost_New tot_cost_New + 1                                                              ;;add new cost to total cost
               set infra_F_age 1                                                                                            ;;update the state (age) of infrastructure
               set Infra_flood 1                                                                                            ;;update the state of the patch. Now the patch contains a piece of infrastructure                                                                                    ;;set new probability of failure = 0
             ]
           ]
           ask ?2 [
             if distance_metric_New_A4 > random-float 1 and tot_cost_New < bud_new [              ;;if total cost until now is lower than budget for new investments, then create new infra in this patch
               set tot_cost_New tot_cost_New + 1                                                              ;;add new cost to total cost
               set infra_S_age 1                                                                                            ;;update the state (age) of infrastructure
               set Infra_supply 1                                                                                            ;;update the state of the patch. Now the patch contains a piece of infrastructure                                                                                    ;;set new probability of failure = 0
             ]
           ]


         ])
       ]

end


;############################################################################
;;Districts evaluate the potential benefits (gains- costs) of each action today and in the future using a discount rate
;; these cost and benefits are the results of conducting a single (e.g protesting) or multiple actions (e.g protesting and adapting)
;############################################################################
to update-lorenz-and-gini ;;;obtained from the netlogo library model "Wealth distribution"
  let sorted-V sort [V] of patches with [district_here? = TRUE]
  let total-V sum sorted-V


  let V-sum-so-far 0
  let index_V 0
  set gini_V 0
  set lorenz-points_V []

  ;; now actually plot the Lorenz curve -- along the way, we also
  ;; calculate the Gini index.
  ;; (see the Info tab for a description of the curve and measure)
  let num-people count patches with [district_here? = TRUE]
  repeat num-people [

    set V-sum-so-far (V-sum-so-far + item index_V sorted-V)
    if total-V > 0 [
      set lorenz-points_V lput ((V-sum-so-far / total-V) * 100) lorenz-points_V
      set index_V (index_V + 1)
      set gini_V gini_V + (index_V / num-people) - (V-sum-so-far / total-V)
    ]
  ]
end


to update_globals_and_reporters
  set max_v max [V] of patches with [district_here? = TRUE] ;max vulnerability of neighborhoods
  set max_protest_F max [protestas_here_F] of patches with [district_here? = TRUE]
  if max_v = 0 [set max_v 1]

  update-lorenz-and-gini ;;update innequality state
   set max_damage max [exposure_F + exposure_S] of patches with [district_here? = TRUE]              ;;Calculate mean damage of city in a time-stepy cakculating the mean damage per year.

  if ticks > 400 [
    set EfficiencyIndex (mean [total_exposure_S + total_exposure_F] of patches with [district_here? = TRUE]) / count patches with [district_here? = TRUE]
    set EfficiencyIndex_S precision ((sum [total_exposure_S] of patches with [district_here? = TRUE]) / count patches with [district_here? = TRUE]) 4
    set EfficiencyIndex_F precision ((sum [total_exposure_F] of patches with [district_here? = TRUE]) / count patches with [district_here? = TRUE] ) 4

    set StateinfraIndex_S StateinfraIndex_S + 0.01 * (count patches with [infra_supply = 1 and p_failure_S < 0.6])
    set StateinfraIndex_F StateinfraIndex_F + 0.01 * (count patches with [infra_flood = 1 and p_failure_F < 0.6])

    set StateinfraAgeIndex_S StateinfraIndex_S + 0.01 * (mean [infra_S_age] of patches with [infra_supply = 1 and p_failure_S < 0.6])
    set StateinfraAgeIndex_F StateinfraIndex_F + 0.01 * (mean [infra_F_age] of patches with [infra_flood = 1 and p_failure_F < 0.6])


    set socialpressureIndex_S precision (mean [socialpressureTOTALIndex_S] of patches with [district_here? = TRUE]) 3
    set socialpressureIndex_F precision (mean [socialpressureTOTALIndex_F] of patches with [district_here? = TRUE]) 3

    set InequalityExposureIndex InequalityExposureIndex + 0.01 * gini_V
  ]

  set C11max ifelse-value (max [C11-Efficiencia] of patches > C11max)[max [C11-Efficiencia] of patches][C11max]                                               ;#update ideal points by setting the maximum of the natural (physical) scale
  set C12max ifelse-value (max [C12-Social_pressure] of patches > C12max)[max [C12-Social_pressure] of patches][C12max]
  set C13max 100

  set C21max ifelse-value (max [C21-need] of patches > C21max) [max [C21-need] of patches][C21max]
  set C22max ifelse-value (max [C22-Social_pressure] of patches > C22max)[max [C22-Social_pressure] of patches][C22max]
  set C23max 100

  set C31max ifelse-value (max [C31-Efficiencia] of patches  > C31max) [max [C31-Efficiencia] of patches][C31max]
  set C32max ifelse-value (max [C32-Social_pressure] of patches > C32max)[max [C32-Social_pressure] of patches][C32max]
  set C33max 100

  set C41max ifelse-value (max [C41-need] of patches > C41max)[max [C41-need] of patches ][C41max]
  set C42max ifelse-value (max [C42-Social_pressure] of patches > C42max)[max [C42-Social_pressure] of patches][C42max]
  set C43max 100
end

to update_state_infrastructure
  ask patches [
    if Infra_flood = 1[                                      ;;for patches with infrastructure, its age increases in one unit every tick
      set infra_F_age infra_F_age + 1
      set P_failure_F 1 - exp(- infra_F_age / 100)             ;;update failure probability
    ]
    if Infra_supply = 1[
      set infra_S_age infra_S_age + 1
      set P_failure_S 1 - exp(- infra_S_age / 100)
    ]

    if Infra_flood = 0[                                      ;;for patches with infrastructure, its age increases in one unit every tick
      set infra_F_age 0
      set P_failure_F 1
    ]

    if Infra_supply = 0[
      set infra_S_age 0
      set P_failure_S 1
    ]

  ]
end

;###############################################################
to export_view  ;;export snapshots of the landscape
  let directory "c:/Users/abaezaca/Documents/MEGADAPT/ABM_V2/landscape_pics/"
  export-View  word directory  word GOVERNMENT_DECISION_MAKING word landscape-type "_infrastructure.png"
end

;###############################################################
to clear-2Dview
  ask patches[Landscape_visualization]
end

;###############################################################
to-report  log-normal [#mu #sigma]
  let beta ln (1 + ((#sigma ^ 2) / (#mu ^ 2)))
  let x exp (random-normal (ln (#mu) - (beta / 2)) sqrt beta)
  report x
end
;###############################################################
to-report max_rain_recorded [p_rain_pro]

let ff 0
let hh_rain []
while [ff < 10000] [
  set hh_rain lput (log-normal 1 p_rain_pro) hh_rain
  set ff ff + 1
]
report (max hh_rain)
end


to read_weightsfrom_matrix
  set matrix_A matrix:from-row-list [                                                                                               ;read supermatrix

[0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.45  0.06  0.45  0.38]
[0.00  0.00  0.00  0.00  0.45  0.06  0.45  0.38  0.00  0.00  0.00  0.00]
[0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.05  0.44  0.05  0.13]
[0.00  0.00  0.00  0.00  0.05  0.44  0.05  0.13  0.00  0.00  0.00  0.00]
[0.00  0.00  0.00  0.26  0.00  0.26  0.00  0.22  0.00  0.00  0.00  0.00]
[0.00  0.05  0.00  0.64  0.08  0.00  0.05  0.08  0.00  0.00  0.00  0.00]
[0.00  0.58  0.00  0.00  0.00  0.05  0.00  0.19  0.00  0.00  0.00  0.00]
[0.00  0.37  0.00  0.10  0.42  0.19  0.45  0.00  0.00  0.00  0.00  0.00]
[0.00  0.00  0.14  0.00  0.00  0.00  0.00  0.00  0.00  0.26  0.00  0.32]
[0.05  0.00  0.53  0.00  0.00  0.00  0.00  0.00  0.13  0.00  0.08  0.13]
[0.58  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.05  0.00  0.05]
[0.37  0.00  0.33  0.00  0.00  0.00  0.00  0.00  0.38  0.19  0.42  0.00]
  ]


  set matrix_B (matrix:times matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A)    ;calculate limit matrix
  print matrix:pretty-print-text matrix_A
  print matrix:pretty-print-text matrix_B
  let w_11_demanda_F_NW item 10 sort (matrix:get-row matrix_B 8)                                                                    ;assige weights from the rows of the limit matrix
  let w_12_presion_F_NW item 10 sort (matrix:get-row matrix_B 11)
  let w_13_estado_F_NW item 10 sort (matrix:get-row matrix_B 9)
  let w_21_necesidad_F_NW item 10 sort (matrix:get-row matrix_B 10)
  let w_22_presion_F_NW item 10 sort (matrix:get-row matrix_B 11)
  let w_23_estado_F_NW item 10 sort (matrix:get-row matrix_B 9)

  let w_31_demanda_S_NW item 10 sort (matrix:get-row matrix_B 4)
  let w_32_presion_S_NW item 10 sort (matrix:get-row matrix_B 7)
  let w_33_estado_S_NW item 10 sort (matrix:get-row matrix_B 5)


  let w_41_necesidad_S_NW item 10 sort (matrix:get-row matrix_B 6)
  let w_42_presion_S_NW item 10 sort (matrix:get-row matrix_B 7)
  let w_43_estado_S_NW item 10 sort (matrix:get-row matrix_B 5)


  let tot_weight_1_F (w_11_demanda_F_NW + w_12_presion_F_NW + w_13_estado_F_NW)                                                    ;calculate total sum of weights for normalization
  let tot_weight_2_F (w_21_necesidad_F_NW + w_22_presion_F_NW + w_23_estado_F_NW)
  let tot_weight_3_S (w_31_demanda_S_NW + w_32_presion_S_NW +  w_33_estado_S_NW)
  let tot_weight_4_S (w_41_necesidad_S_NW + w_42_presion_S_NW + w_43_estado_S_NW)

  set w_11_demanda_F w_11_demanda_F_NW / tot_weight_1_F                                                                           ;normalize weights with respect to each action
  set w_12_presion_F w_12_presion_F_NW / tot_weight_1_F
  set w_13_estado_F w_13_estado_F_NW / tot_weight_1_F

  set w_21_necesidad_F w_21_necesidad_F_NW / tot_weight_2_F
  set w_22_presion_F w_22_presion_F_NW  / tot_weight_2_F
  set w_23_estado_F w_23_estado_F_NW  / tot_weight_2_F

  set w_31_demanda_S w_31_demanda_S_NW / tot_weight_3_S
  set w_32_presion_S w_32_presion_S_NW / tot_weight_3_S
  set w_33_estado_S w_33_estado_S_NW / tot_weight_3_S

  set w_41_necesidad_S w_41_necesidad_S_NW / tot_weight_4_S
  set w_42_presion_S w_42_presion_S_NW / tot_weight_4_S
  set w_43_estado_S w_43_estado_S_NW / tot_weight_4_S




  print word "w_11_demanda_F=" w_11_demanda_F
  print word "w_12_presion_F= " w_12_presion_F
  print word "w_13_estado_F= " w_13_estado_F
  print word "w_21_necesidad_F= " w_21_necesidad_F
  print word "w_22_presion_F= " w_22_presion_F
  print word "w_23_estado_F= " w_23_estado_F
  print word "w_31_demanda_S= " w_31_demanda_S
  print word "w_32_presion_S= " w_32_presion_S
  print word "w_33_estado_S= " w_33_estado_S
  print word "w_41_necesidad_S=" w_41_necesidad_S
  print word "w_42_presion_S=" w_42_presion_S
  print word "w_43_estado_S=" w_43_estado_S


end

to update_weights                                   ;generate a change in the supermatrix due to a change in pair comparisong of criterias with respect to action "nueva_F"


 matrix:set matrix_A 9 0 0.814212784               ;change values of weights of cluster F (inundaciones) with respect to create new_F
 matrix:set matrix_A 10 0 0.113982647
 matrix:set matrix_A 11 0 0.113982647

 set matrix_B (matrix:times matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A matrix_A)  ;generate new limit matrix

 let w_11_demanda_F_NW item 10 sort (matrix:get-row matrix_B 8)                      ;set new weights
 let w_12_presion_F_NW item 10 sort (matrix:get-row matrix_B 11)
 let w_13_estado_F_NW item 10 sort (matrix:get-row matrix_B 9)
 let w_21_necesidad_F_NW item 10 sort (matrix:get-row matrix_B 10)
 let w_22_presion_F_NW item 10 sort (matrix:get-row matrix_B 11)
 let w_23_estado_F_NW item 10 sort (matrix:get-row matrix_B 9)

 let w_31_demanda_S_NW item 10 sort (matrix:get-row matrix_B 4)
 let w_32_presion_S_NW item 10 sort (matrix:get-row matrix_B 7)
 let w_33_estado_S_NW item 10 sort (matrix:get-row matrix_B 5)


 let w_41_necesidad_S_NW item 10 sort (matrix:get-row matrix_B 6)
  let w_42_presion_S_NW item 10 sort (matrix:get-row matrix_B 7)
  let w_43_estado_S_NW item 10 sort (matrix:get-row matrix_B 5)

  let tot_weight_1_F (w_11_demanda_F_NW + w_12_presion_F_NW + w_13_estado_F_NW)
  let tot_weight_2_F (w_21_necesidad_F_NW + w_22_presion_F_NW + w_23_estado_F_NW)
  let tot_weight_3_S (w_31_demanda_S_NW + w_32_presion_S_NW +  w_33_estado_S_NW)
  let tot_weight_4_S (w_41_necesidad_S_NW + w_42_presion_S_NW + w_43_estado_S_NW)

  set w_11_demanda_F w_11_demanda_F_NW / tot_weight_1_F
  set w_12_presion_F w_12_presion_F_NW / tot_weight_1_F
  set w_13_estado_F w_13_estado_F_NW / tot_weight_1_F

  set w_21_necesidad_F w_21_necesidad_F_NW / tot_weight_2_F
  set w_22_presion_F w_22_presion_F_NW  / tot_weight_2_F
  set w_23_estado_F w_23_estado_F_NW  / tot_weight_2_F

  set w_31_demanda_S w_31_demanda_S_NW / tot_weight_3_S
  set w_32_presion_S w_32_presion_S_NW / tot_weight_3_S
  set w_33_estado_S w_33_estado_S_NW / tot_weight_3_S


  set w_41_necesidad_S w_41_necesidad_S_NW / tot_weight_4_S
  set w_42_presion_S w_42_presion_S_NW / tot_weight_4_S
  set w_43_estado_S w_43_estado_S_NW / tot_weight_4_S



 print word "w_11_demanda_F=" w_11_demanda_F
 print word "w_12_presion_F= " w_12_presion_F
 print word "w_13_estado_F= " w_13_estado_F
 print word "w_21_necesidad_F= " w_21_necesidad_F
 print word "w_22_presion_F= " w_22_presion_F
 print word "w_23_estado_F= " w_23_estado_F
 print word "w_31_demanda_S= " w_31_demanda_S
 print word "w_32_presion_S= " w_32_presion_S
 print word "w_33_estado_S= " w_33_estado_S
 print word "w_41_necesidad_S=" w_41_necesidad_S
 print word "w_42_presion_S=" w_42_presion_S
 print word "w_43_estado_S=" w_43_estado_S

end

;###############################################################
;###############################################################
;End of Code
;###############################################################
;###############################################################
@#$#@#$#@
GRAPHICS-WINDOW
280
27
836
604
-1
-1
5.46
1
10
1
1
1
0
1
1
1
0
99
0
99
1
1
1
ticks
30.0

BUTTON
44
30
107
63
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
107
30
170
63
NIL
GO
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
169
30
232
63
NIL
GO
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

CHOOSER
24
478
279
523
Visualization
Visualization
"Infrastructure_F" "Infrastructure_S" "Spatial priorities maintanance F" "Spatial priorities new F" "Spatial priorities maintanance S" "Spatial priorities new S" "Vulnerability" "Social Pressure_F" "Social Pressure_S" "Districts" "Harmful Events"
2

PLOT
840
25
1040
175
Rainfall
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot R"

CHOOSER
20
226
255
271
GOVERNMENT_DECISION_MAKING
GOVERNMENT_DECISION_MAKING
"Social Benefit" "State of infrastructure" "Response to Social Pressure"
2

PLOT
859
333
1232
559
Mean vulnerability
NIL
NIL
0.0
1.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "if ticks > 10 [plot mean [V] of patches with [district_here? = TRUE]]"
"pen-1" 1.0 0 -11221820 true "" "if ticks > 10 [plot mean [exposure_F] of patches with [district_here? = TRUE]]"
"pen-2" 1.0 0 -6459832 true "" "if ticks > 10 [plot mean [exposure_S] of patches with [district_here? = TRUE]]"

PLOT
836
576
1171
823
Protests
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -11221820 true "" "plot mean [protestas_here_F] of patches with [district_here? = TRUE]"
"pen-1" 1.0 0 -8431303 true "" "plot mean [protestas_here_S] of patches with [district_here? = TRUE]"

SLIDER
31
377
216
410
New_infra_investment
New_infra_investment
0
500
100
1
1
NIL
HORIZONTAL

CHOOSER
34
594
228
639
Initial-Condition-Infrastructure
Initial-Condition-Infrastructure
"Perfect" "Worse" "intermedia"
1

PLOT
840
173
1040
323
GINI
NIL
NIL
0.0
10.0
0.0
1.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot gini_V / count patches with [district_here? = TRUE]"

PLOT
1040
174
1240
324
Lorenz Curve
NIL
NIL
0.0
100.0
0.0
100.0
false
false
"" ""
PENS
"LC" 1.0 0 -2674135 true "" "plot-pen-reset\nset-plot-pen-interval 100 / count patches with [district_here? = TRUE]\nplot 0\nforeach lorenz-points_V plot"
"pen-1" 100.0 0 -16777216 true "plot 0\nplot 100" ""

SLIDER
31
410
217
443
p_rain
p_rain
0.25
1.5
0.5
0.05
1
NIL
HORIZONTAL

BUTTON
282
620
387
655
NIL
clear-2Dview
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

BUTTON
285
657
386
690
NIL
export_view
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

TEXTBOX
32
140
211
175
Define Scenarios
20
0.0
1

TEXTBOX
41
295
262
322
Define Parameter Values
18
0.0
1

SLIDER
31
345
216
378
maintenance
maintenance
0
500
130
1
1
NIL
HORIZONTAL

CHOOSER
20
183
255
228
landscape-type
landscape-type
"closed watershed" "gradient" "many hills"
2

TEXTBOX
72
447
260
471
Visualization
16
0.0
1

PLOT
1180
584
1380
734
plot 1
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -8990512 true "" "plot count patches with [infra_flood = 1 and p_failure_F < 0.9]"
"pen-1" 1.0 0 -6459832 true "" "plot count patches with [infra_supply = 1 and p_failure_S < 0.9]"

INPUTBOX
70
72
188
140
semilla-aleatoria
48569
1
0
Number

@#$#@#$#@
# MEGADAPT PROTOTYPE ABM
## WHAT IS IT?
This model simulates an urban landscape composed of a group of interconnected districts subjected to hazardous events. These events when happen cause damage and wealth lost to the districts. The districts may or may not have infrastructure in thier patch. Having an infrastructure piece can reduce the probability of hazards.  that respond to this burden by deciding how to best allocate time to undertake 3 possible actions: they can 1) try to adapt to this hazardous environment by modifying their local environment and thus reduce the potential damage of future hazardous events. 2) They can also try to demand actions from the government by allocating time to protesting, with the aim that govertment will maitain the infrastructure and thus reduce the changes of future events. Finally, 3) they spend time participating in social organizations to create and maintain social capital. Social capital can boost the rate of adaptation, and the magnitude of protesting.

The objective of the model is to understand and exemplify the role of “government prioritization strategies” and “decision-making process” on the vulnerability, economic efficiency and social inequality of a coupled urban-infrastructure system.

## HOW IT WORKS
Every time-step (tick) a hazardous event may occur with probability PHn, independently for each district. Hazardous events when do occur they produce a damage proportional to the magnitude of the event.

The Government evaluates each district and the state of the infrastructure in which the district is located to decide where to invest the economic resources constrained by a budget. It does so by computing a distance metric between the actual state of the system evaluated for a set of indicators or criterion and the ideal state from the government perspective. The current version includes three criterion for the two actions:
1) The state of infrastructure, using its age as proxy for failure
2) The state of the social satisfaction, using the number of protest registered in the area surrounding a patch, and
3) The economic efficiency of each investment, using the number of neighborhoods that would beneficiate per dollar invested as indicator of efficiency.

Each action (To maintain or create new one) is associated with a criteria by a weight parameter that define the importance or level of prioritization of this factor in the decision. The set of weight parameters that linked each criteria to actions (invest in new infrastructure or maintain new pieces) define a "decision strategy".
A strategy to control social pressure for example, would weight more heavily on reducing the number of protests, for example that efficiency distribute dollar by only the age of the infrastructure.

Every time-step, districts will allocate time to undertake different actions to reduce damage to produce income and to have leisure time. The proportion of time that each n invests in these actions indicates its intensity in the landscape.
Each neighborhood will carried out a particular strategy. This strategy consists of dividing the time devoted to four actions: protesting LP, modifying the local environment to seek adaptation LA, spend time in social organizations LO and finally do nothing. Each district will evaluate the “optimal” strategy to use every time step by either maximizing benefits of each action (cost-benefit scenario) or learning from other district’s experience (social learning scenarios).


## HOW TO USE IT

The interface is composed of a set of “choosers” to define scenarios and “sliders” to set parameter values. It also includes a set of plots to show the dynamics of the different socio economic indices and the state of the infrastructure and the damage and vulnerability of the city.

Within the 2D view, a chooser called “Visualization” controls the type of information contained in each patch in the landscape that will be displayed along with the button “clear-2d-view”.
After defining scenarios and parameter values press the “Setup” button to create the landscape, the districts and the initial state of the infrastructure. Then press the “GO” button to simulate hazardous events and the response of districts and government.



##Define scenarios (Choosers)

To define scenarios of government and districts decision making.

### DISTRICTS_DECISION_MAKING

Define the type of decision making process behind the allocation of time in each district.

**Protesters**: In this setting protesting is the only activity of neighborhoods can take. The probability that a neighborhood would protest is equal to the time devoted to protest Ld, which is defined proportionally to the average number of hazardous events recorded in the past 10 time-steps (ticks).
**Cost-Benefits**: Each district evaluate each possible time allocation strategy by comparing the expected cost and gains of each action assuming expectation of risk and adaptation under government maintenance and a new magnitude-damage relationship.
**Social-learning**: Each neighborhood divides the time using a particular strategy. Every time-steps agents evaluate the performance observed using its strategy against the performance of other neighborhoods in a radius of 3 patches. When the level of exposure of neighborhoods is lower that the level of themselves they adopt the strategy of the more successful neighborhood. The performance is evaluate by the number of hazardous events recorded in the past 10 time steps.
**Social-learning-Typology-of-districts**: Similar to Social learning but the division of labor is fixed; that is the time strategy is constant for a type of neighborhood. We define 5 types of neighborhoods:

_Individual change seekers_: District that devote only time to change their own environment without spending time in social organizations.

_Endogenous change seekers_: these are districts that devote more time to changing their own environment but also devote time to social organization. They recognize the importance of social capital in accelerating changes. They devote low time to protesting.

_Exogenous change seekers_: This type of districts spends more time in social organization and protesting seeking to change government distribution of resources for them. They recognized the importance of social capital and therefore devote time to social organization is detriment of changing their own environment. They are represented with a red color in the landscape.

_Protester_: Similar to exogenous change seekers but this type of districts do not devote time to social organization. It does this only by demanding or protesting individually to the government.

_Apathetic_: These are districts that do not devote time to any activity.


### GOVERNMENT_DECISION_MAKING
Define government prioritization for decision making

**Economic-Efficiency**: government place more emphasis on district that generate more benefits to people determine by the number of districts beneficiated by dollar invested.

**State-Infrastructure**: government is more interested in allocated more resources with aged infrastructure or areas that lacks of infrastructure provision.

**Response to Social Pressure**: In this scenarios government is more interested in reducing the social pressure or the number of protests occur in each district.


###VISUALIZATION
**Topography**: Visualized the watershed by coloring based on altitude where lighter grey to white represent higher places

**Infrastructure**: Visualize the age of the infrastructure in the landscape using a grey scale. Areas with newer infrastructure show lighter tones of grey.

**Vulnerability**: Shows the value of the vulnerability index in a blue scale. Lighter tones indicate higher vulnerability

**Social Pressure**: Display the time districts devote to protesting. Lighter tones of red represent higher time protesting.

**Adaptation**: Display the time districts devote to changing their local enviroment. Lighter tones of magenta represent higher time adapting.


**Type Actor**: Display colors in the patches based on the type of district.
-_Individual Adaptator_: light blue
-_Protesters_: red
-_Endogenous change seekers_: turquoise
-_Exogenous change seekers_: pink
-_Indifferent_: white


###Initial-Condition-Infrastructure
To investigate the resilience of the system to the inertia of the cost forced by an aging infrastructure, we assumed three different initial conditions regarding the age of the infrastructure at the beginning of the simulation:

**Perfect**: this represent an scenario with an ideal situation, where infrastructure is new (Age = 1 year)

**Intermedia**: this is a situation in between the perfect and the worse, where the Age = 50 years

**Worse**: This is a scenario with a very aged system (mean age = 100 years)



##Sliders:
**Budget-Maintenance**: To set the budget for maintenance by defining % of wealth collected (a sort of an income taxes)

**Budget-Investment**: to set the budget for new infrastructure by defining a % of total resources needed to provide infrastructure to every neighborhood

**Effective_modE**: It controls the rate at which labor designated to adaptation translate into modification of the magnitude-cost function.

**Discount_rate**: parameter that controls the time horizon to calculate expected gains.

**N_linear_prot**: define the non-linearity of the value function of social criteria. The larger this parameter is the larger the number of protest must be to trigger an action.

**mean_R**: set the mean of a normal distribution that will generate random realizations of climatic events


## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.2.1
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="ABMV2.0_snapshotgradient" repetitions="1" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="500"/>
    <metric>EfficiencyIndex</metric>
    <metric>InequalityExposureIndex</metric>
    <metric>ExposureIndex</metric>
    <metric>EfficiencyIndex_S</metric>
    <metric>EfficiencyIndex_F</metric>
    <metric>StateinfraIndex_S</metric>
    <metric>StateinfraIndex_F</metric>
    <metric>socialpressureIndex_S</metric>
    <metric>socialpressureIndex_F</metric>
    <metric>StateinfraAgeIndex_S</metric>
    <metric>StateinfraAgeIndex_F</metric>
    <enumeratedValueSet variable="p_rain">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="New_infra_investment">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="landscape-type">
      <value value="&quot;gradient&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="GOVERNMENT_DECISION_MAKING">
      <value value="&quot;Social Benefit&quot;"/>
      <value value="&quot;State of infrastructure&quot;"/>
      <value value="&quot;Response to Social Pressure&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="maintenance">
      <value value="60"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@