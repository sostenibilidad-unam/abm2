require(tgp)
s1 <- round(lhs(20000, rbind(c(0,1), c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1))),digits = 2)


colnames(s1)<-c("w_11_demanda_F",	"w_12_presion_F",	"w_21_necesidad_F",	"w_22_presion_F",	"w_31_demanda_S",	"w_32_presion_S",	"w_41_necesidad_S",	"w_42_presion_S")

s2<-  s1[which(s1[,1]+s1[,2] < 1),]
s3<-s2[which(s2[,3]+s2[,4]<1),]
s4<-s3[which(s3[,5]+s3[,6]< 1),]
s5<-s4[which(s4[,7]+s4[,8]< 1),]
write.csv(x = s5,file = "sampling_scenarios_Weights.csv")


#new scheme to obtain a new set of weights and decition metric
s1 <- data.frame(round(lhs(2000, rbind(c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9), c(0,0.9),c(0,0.9),c(0,0.9),c(0,0.9),c(0,0.9),c(0,0.9))),digits = 2))

colnames(s1)<-c("w_1_demanda_F",	"w_2_presion_F",	"w_3_stateInfra_F","w_4_necesidad_F",	"w_5_demanda_S",	"w_6_presion_S","w_7_stateInfra_S",	"w_6_necesidad_S","A_repair_F","A_new_F","A_repair_S","A_new_S")

s1[,1:8]<-s1[,1:8]/rowSums(s1[,1:8])

s1[,9:12]<-s1[,9:12]/rowSums(s1[,9:12])


write.csv(x = s1,file = "sampling_scenarios_new_Weights.csv")
