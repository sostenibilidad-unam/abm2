require(tgp)
s1 <- round(lhs(500, rbind(c(0,0.9), c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1),c(0,1))),digits = 1)
s2<-  s1[which(s1[,1]+s1[,2] < 1),]
s3<-s2[which(s2[,3]+s2[,4]<1),]
s4<-s3[which(s3[,5]+s3[,6]< 1),]
s5<-s4[which(s4[,7]+s4[,8]< 1),]
write.csv(x = s5,file = "~/MEGADAPT/ABM_V2/sampling_scenarios_Weights.csv")
