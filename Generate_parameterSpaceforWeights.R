require(tgp)
s1 <- round(lhs(20000, rbind(c(0,1), c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1))),digits = 2)


colnames(s1)<-c("w_11_demanda_F",	"w_12_presion_F",	"w_21_necesidad_F",	"w_22_presion_F",	"w_31_demanda_S",	"w_32_presion_S",	"w_41_necesidad_S",	"w_42_presion_S")

s2<-  s1[which(s1[,1]+s1[,2] < 1),]
s3<-s2[which(s2[,3]+s2[,4]<1),]
s4<-s3[which(s3[,5]+s3[,6]< 1),]
s5<-s4[which(s4[,7]+s4[,8]< 1),]
write.csv(x = s5,file = "sampling_scenarios_Weights.csv")


#new scheme to obtain a new set of weights and decition metric
#1) varying W but keeping D constant
s1 <- lhs(2000, rbind(c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9)))
aa<-cbind(rep(0.25,200),rep(0.25,200),rep(0.25,2000),rep(0.25,2000))
s1 <- data.frame(round(cbind(s1,aa),digits = 3))

colnames(s1)<-c("w_1_demanda",	"w_2_presion_F",	"w_3_stateInfra_F","w_4_necesidad_F",	"w_6_presion_S","w_7_stateInfra_S",	"w_6_necesidad_S","A_new_F","A_new_S","A_repair_F","A_repair_S")

s1[,1:7]<-s1[,1:7]/rowSums(s1[,1:7])

s1[,8:11]<-s1[,8:11]/rowSums(s1[,8:11])

write.csv(x = s1,file = "~/MEGADAPT/abm2/sampling_scenarios_var_W.csv")

#1) varying W and D 
s2 <- data.frame(round(lhs(2000, rbind(c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9))),digits = 2))

colnames(s2)<-c("w_1_demanda",	"w_2_presion_F",	"w_3_stateInfra_F","w_4_necesidad_F",	"w_6_presion_S","w_7_stateInfra_S",	"w_6_necesidad_S","A_new_F","A_new_S","A_repair_F","A_repair_S")

s2[,1:7]<-s2[,1:7]/rowSums(s2[,1:7])

s2[,8:11]<-s2[,8:11]/rowSums(s2[,8:11])


write.csv(x = s2,file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_var_WandD.csv")


#1) varying D but keeping W constant
s3<-lhs(2000, rbind(c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9)))
aa<-cbind(rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,200),rep(0.25,2000),rep(0.25,2000))
s3 <- data.frame(round(cbind(aa,s3),digits = 3))

colnames(s3)<-c("w_1_demanda",	"w_2_presion_F",	"w_3_stateInfra_F","w_4_necesidad_F",	"w_6_presion_S","w_7_stateInfra_S",	"w_6_necesidad_S","A_new_F","A_new_S","A_repair_F","A_repair_S")
s3[,1:7]<-s3[,1:7]/rowSums(s3[,1:7])
s3[,8:11]<-s3[,8:11]/rowSums(s3[,8:11])


write.csv(x = s3,file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_var_D.csv")



write.csv(x = rbind(s1,s2,s3),file = "~/MEGADAPT/abm2/sampling_scenarios_Weights_all.csv")
