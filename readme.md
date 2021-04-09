# PCB Autorouting - Genetic AI algorithm report

The task was about using genetic AI algorithm in order to autoroute PCB in the best possible way, which means minimal path lengths, minimal number of segments and no intersections. Before establishing the best parameters to use in the program, we have to establish what some of GA (genetic algorithms) terms mean in our program:
* **specimen/chromosome** – one solution, which is a PCB with all the paths connecting given points.
* **population** – set of specimens, representing one generation
* **gene** – a component of a chromosome. In our task, gene is represented as a single path of the PCB. Mutation will work on the gene level, making changes in segments inside of the path. 

Each path is represented as a list of segments. Each of segment consist of start and end point. There is also a board, which determines what pairs of points are to be connected and what is the available space.

When initialising the population, a pathfinding algorithm is used. The algorithm is based on random search, with a bigger chance of going in direction of the destination. There are three main points to be mentioned about the algorithm:
* Each generated segment have to be in different orientation than its neighbour.
* When determining the length of the segment, algorithm takes the distance to the border into consideration. It means that **paths out of the border will not exist**. This approach have its pros and cons – initial specimens will be more realistic and there is less space to travel, which without capping the number of segments could lead to infinite time of finding the path. On the other hand, it limits the exploration potential – paths out of border can actually be close to the solution and a proper mutation could bring the path back on the board.
* There is a manually set cap on the maximal number of segments in path in order to speed up the initialisation and mutations, which use the pathfinding algorithm. It can be removed but it would slower the execution drastically.

## Start parameters

In each test simulation will be run 10 times for given parameters:
| | |
|-|-|
| Generations limit     | 75   |
| Crossover probability | 0.7  |
| Mutation probability  | 0.15 |
| Reroll probability    | 0.15 |
| Population size       | 300  |

If tests will prove a better parameter, it will be used in next sections. Every test which is not signed with task number, is performed for Task 1, which is the most general and common case and therefore is very viable for test purposes.

## Fitness function

The fitness function takes 3 parameters into consideration – length of the paths, the count of the segments and the count of intersections. 
* Length is the most basic parameter to be considered, so its weight has been set to **1** – it means that path containing 1 segment which connect points (10, 20) and (20, 20) will get 10 fitness penalty from length.
* We want our paths to be as simple as possible. In order to do that, there has to be a penalty for every segment so AI will like simpler solutions more. The penalty has been experimentally set to **20** per segment and works as expected.
* Intersections of paths should never exist for a solution to be a valid PCB. To not restrict pathfinding to prevent paths from intersecting, which would lead to worse exploration, we have to properly penalise every intersection. The value of **1000** works as expected, promoting solutions with the least number of intersections.

|             |Fitness penalty|
|-------------|---------------|
|Path lengths |1              |
|Segment count|20             |
|Intersections|1000           |

> **Note**: Values can be easily changed through the parameters passed to the main function, which can be used e.g. to optimise the result only for path lengths, without considering number of segments. The values could not work that well in other scenarios that the given tasks – for instance when board size would be so big that getting 1000 points penalty by intersecting another path is still better than finding another solution with bigger number of segments and longer paths.

## Selection

### Roulette wheel
|                  |Genetic algorithm [10x]|
|------------------|-----------------------|
|Best              |4488                   |
|Worst             |8360                   |
|Average           |6283                   |
|Standard deviation|1278                   |
|Survivability     |10%                    |

The interesting thing about roulette wheel selection is that in last population the best solution is not present in most of the cases. Also, the population is really diverse. It means that the survivability is low. In case of this experiment, only 1 of last populations had its best specimen.

### Tournament

|Tournament size|Best|Worst|Average|Standard deviation|Survivability|
|--------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|2|4562|9462|6219|1512|60%|
|3|1552|7452|5117|1443|80%|
|**4**|2538|7434|5512|1410|100%|
|5|3472|8408|5596|1207|100%|
|6|4452|7546|5629|1111|100%|
|7|3524|6576|5112|1167|100%|
|8|3626|7514|5418|1076|100%|
|10|4476|8460|6213|1386|100%|
|12|3540|7472|5709|1205|100%|
|15|4474|7380|5425|1080|100%|
|25|5406|8376|6780|952|100%|
|50|2432|9332|6388|1800|100%|
|75|4452|9334|6803|1476|100%|

Low tournament size leads to lower survivability. This is because there is lower chance of  drawing a specific specimen into the tournament. The bigger the tournament size, the greater survivability. However, it has a downside – with bigger tournament size, the population is becoming very homogenous really fast. It means that mutation will be the main source of upgrades, which is not good - evolution should mainly consist of crossovers. To preserve a good survivability with diverse population and taking average fitness score into consideration, **tournament size of 4 was chosen as the best**. Roulette wheel selection is visibly worse than tournament selection and it has really bad survivability, which leads to losing the best specimens, so population average fitness may regress.

## Population

> Changing population size will affect time of execution, so for fair comparison, now each simulation will run for 25s rather than for 75 generations.

|Population size|Best|Worst|Average|Standard deviation|Survivability|
|--------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|25|5514|14684|8032|2754|90%|
|50|4692|11570|7983|2012|100%|
|75|5426|9530|7237|1205|100%|
|100|3476|7526|5826|1342|100%|
|150|3506|10510|6726|1918|100%|
|200|3520|8572|6036|1892|100%|
|250|3536|8416|5732|1700|100%|
|**300**|3592|7518|6112|1329|100%|
|400|3500|8462|5822|1405|100%|
|500|6408|9392|7660|907|100%|
|600|4514|9476|7597|1835|100%|
|700|4476|10542|7957|1764|100%|
|800|5518|12350|9372|2141|100%|
|1000|7402|18536|11668|4010|100%|

Low population sizes leads to rather bad results. It is because we do not have good diversity, so we do not have much to work with. Bigger populations provide diversity, but at some point they start to slow down the evolution dramatically. In long run, bigger population size could provide better results, but the time required would be much longer. Because we are considering time as a important factor, for a chosen interval of time **population of 300 specimens** seems to be a good choice looking at the tendency of average fitness scores.

## Crossover

### Crossover with random genes from both parents
|Crossover prob.|Best|Worst|Average|Standard deviation|Survivability|
|--------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|10%|5518|9620|6952|1187|100%|
|20%|4484|9374|6306|1370|100%|
|30%|3568|8606|7013|1710|100%|
|40%|4470|8524|5702|1308|100%|
|50%|3500|6580|5319|1364|100%|
|**60%**|1686|6490|5139|1368|90%|
|70%|4454|9462|5627|1605|90%|
|80%|2480|8468|5906|1631|100%|
|90%|4542|6484|5548|636|100%|
|100%|3594|8456|5719|1638|100%|

### Crossover with half genes from the first parent and half from the second parent
|Crossover prob.|Best|Worst|Average|Standard deviation|Survivability|
|--------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|10%|4558|11618|7348|2000|90%|
|20%|5566|10500|7608|1507|80%|
|30%|4542|10574|6946|1632|90%|
|40%|5518|15714|9286|3375|100%|
|50%|4514|10550|7822|2188|90%|
|60%|4492|11440|8198|2061|90%|
|70%|5480|12532|7789|2053|100%|
|80%|4538|11526|7355|2139|100%|
|90%|6500|10440|8162|1456|80%|
|100%|5508|10530|7855|1686|90%|

More random crossovers provides much better results. The reason for that may be a better variaty in crossover childrens from the same parents, which may lead to more interesting results. For crossover with random genes, **60% chance of crossover leads to the best results**.

## Mutation

Two types of mutations are implemented - shift, which picks a random segment in a path (but not the edge segments) and shifts it vertically or horizontally, depending on the orientation of the segment. It is also capable of simplifying the path when some specific conditions are met, like shifting a segment into another, closely located one. Another type is reroll - it picks a random segment and rerolls the rest of the path after it. It is way more random, but provides good exploration. At first we have to establish which mutation type is better or the best proportion of them both.

### Reroll/shift mutation proportions
|Reroll prob.|Best|Worst|Average|Standard deviation|Survivability|
|-----------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|100%|1628|8426|5257|1724|90%|
|95%|2506|6450|4579|1257|100%|
|90%|2494|6384|4467|1117|100%|
|85%|3434|7408|4353|1345|90%|
|80%|2442|7406|5042|1691|100%|
|75%|2456|6428|4633|1200|100%|
|70%|2522|5476|4272|1267|100%|
|65%|2526|6382|4665|1097|100%|
|**60%**|2458|5640|3903|1269|100%|
|55%|2442|6386|4837|1055|100%|
|50%|2500|9334|5136|1785|100%|
|45%|2456|8338|4846|2128|80%|
|40%|3460|7398|5711|1658|100%|
|35%|1504|6384|4457|1660|100%|
|30%|3436|9334|5428|1848|100%|
|25%|3450|7360|5329|1418|90%|
|20%|4436|7360|5817|1151|100%|
|15%|3390|8336|5808|1676|100%|
|10%|3456|7360|5518|1272|100%|
|5%|3436|8376|5709|1968|100%|
|0%|3480|10348|6001|1920|100%|

It seems that both types are valuable and **60% of reroll mutation with 40% of shift mutation works the best**. Shift mutation can only preserve or reduce number of segments in the path, so use of reroll to introduce new segments or for a chance of simplification is for sure reasonable. Now we can determine the chance of a given specimen to mutate, that leads to the best results.

### Mutation probability
|Mutation prob.|Best|Worst|Average|Standard deviation|Survivability|
|-------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|90%|1484|4516|2398|1104|80%|
|85%|584|4594|2611|1432|60%|
|80%|1484|3542|2316|781|80%|
|75%|1484|4490|3494|814|90%|
|70%|544|4430|2404|1078|90%|
|65%|542|4488|2507|1246|80%|
|60%|1506|6420|3477|1386|90%|
|55%|1484|5466|2798|1248|90%|
|50%|1484|4450|2880|1150|100%|
|45%|1484|5426|3459|1600|100%|
|40%|1484|4478|3079|1150|100%|
|**35%**|1500|4518|2508|935|100%|
|30%|566|5466|3182|1536|90%|
|25%|1484|5486|3585|1346|100%|
|20%|1496|5472|4246|1450|100%|
|15%|2472|7400|4746|1673|80%|
|10%|2522|7360|4839|1536|100%|
|5%|1544|7380|5129|2062|100%|
|0%|7408|10616|9069|1073|90%|

It is clearly visible that low chances of mutation do not work very well. My implementations of mutation allow only for a single path mutation, so mutations are not very drastic and thus more frequent mutations work better. The average fitness score is not changing after 30% mark and greater mutation probability decreases survivability, so **35% mutation probability was chosen**,

## Number of generations

### Task 1
|Generation count|Best|Worst|Average|Standard deviation|Survivability|
|---------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|50|1484|8358|4469|1669|100%|
|75|1484|5466|3180|1611|100%|
|100|1484|4472|3069|1066|100%|
|150|1484|4446|2591|726|100%|
|200|1484|3470|2396|858|100%|
|300|534|3518|2218|1032|90%|
|400|542|3510|1711|1113|100%|
|500|542|2538|1925|959|100%|

### Task 2
|Generation count|Best|Worst|Average|Standard deviation|Survivability|
|---------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|50|1289|2235|1857|487|100%|
|75|405|2235|1593|744|100%|
|100|1289|2235|1485|396|100%|
|150|1289|2235|1496|391|90%|
|200|1289|1289|1289|0|100%|
|300|1289|1289|1289|0|100%|
|400|397|1289|932|461|100%|
|500|1289|1289|1289|0|100%|

### Task 3
|Generation count|Best|Worst|Average|Standard deviation|Survivability|
|---------------:|:--:|:---:|:-----:|:----------------:|:-----------:|
|50|4634|13718|7212|3556|90%|
|75|4632|12778|6373|2679|90%|
|100|4632|7696|5466|1173|100%|
|150|3784|8658|4950|1330|100%|
|200|3784|10664|5470|2099|100%|
|300|3714|6658|4743|732|100%|

## Comparison with random search

In 10 runs of random search with the same number of specimens investigated as for AI, the best result is nowhere close to the results obtained by the AI. Also, the time was about 6 time longer. It shows that AI outperformes random search, which was expected.

|        |Random search|
|--------|-------------|
|Best    |42870        |
|Worst   |96076        |
|Average |75755        |