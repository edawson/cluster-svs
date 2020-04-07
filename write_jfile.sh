for i in `ls | grep "sv.bedpe"`
do	
	echo $i
	echo "Rscript clustering_index.R $i 2" >> jobfile.txt
done
