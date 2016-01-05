#!/bin/bash


for((i=2;i>=2;i--));do
rundate=`date +%Y%m%d --date="-${i} day"` 
month=`date +%m --date="-${i} day"`

corpusdir="/home/dzn/hd/corpus"
dictdir=${corpusdir}/month_${month}/${rundate}
pytools="/home/dzn/Query"
numbest=10

run_date=${pytools}/query_${rundate}
rm -rf ${run_date}
mkdir ${run_date}

query=恒大夺冠

if [ -d $dictdir ];then
  cindex=${run_date}/seedindex.txt
  corpus=${run_date}/seedcorpus.txt
  touch ${run_date}/seedindex.txt
  touch ${run_date}/seedcorpus.txt 
  for((j=9;j>=0;j--));do
    if [ -d ${dictdir}/topic_cluster_${j} ];then
      if [ -f ${dictdir}/topic_cluster_${j}/seedcorpus.txt ];then
        cat ${dictdir}/topic_cluster_${j}/seedcorpus.txt >> ${run_date}/seedcorpus.txt
      fi
      if [ -f ${dictdir}/topic_cluster_${j}/seedindex.txt ];then
        cat ${dictdir}/topic_cluster_${j}/seedindex.txt >> ${run_date}/seedindex.txt                  
      fi
    fi
  done
  ${pytools}/gensim_query.py -i ${cindex} -c ${corpus} -s ${query} -n ${numbest} -r $run_date > ${run_date}/query.log
else
  echo "Error Message: ${dictdir} is not exists"
  exit 1
fi
  
done


