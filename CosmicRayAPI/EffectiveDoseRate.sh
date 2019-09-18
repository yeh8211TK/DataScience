node "parameters.js" "$1";

for((i=1; i<13; i=i+1))
do
    for((j=1; j<29; j=j+1))
    do
        "node" "CosmicRayAPI.js" "$1" "$i" "$j";
    done
done

echo "檔案執行完成";