Scott Beamer'in [paper](https://people.eecs.berkeley.edu/~krste/papers/beamer-iiswc2015.pdf)'ında iddaa edilen en büyük bottleneck'in instruction window size olduğu tezini test etmek için birkaç deney yaptım ve bunun doğru olmadığını gördüm çünkü instruction window size'ı ne kadar arttırırsam attırayım memory bandwidth utilization'daki artış önemsenmeyecek derecede az oldu. Sonra başka bir [paper](https://seal.ece.ucsb.edu/sites/seal.ece.ucsb.edu/files/publications/hpca-2019-abanti.pdf)'da da aynısını belirttiklerini gördüm.

Şu an gördüğüm kadarıyla vertex centric yazılan programların main bottleneck'i load-load dependency zincirleri. Bu bağımlılıkların da açtığı üç temel sorun var:

- Workload irregularity: Her vertex'in edge sayısı farklı olduğu için, thread'lere atanan işlerde imbalance ortaya çıkıyor.

- Traversal irregularity: Her iterasyonda aktif vertex'ler değiştiği için random memory access'ler oluşuyor ve locality düşüyor öyle olunca da.

- Update irregularity: Her iterasyonda çok az sayıda vertex update edilmesine rağmen her iterasyonda bütün vertex'leri geziyor program. Bu da bir sürü gereksiz hesaplamaya yol açıyor.    

State of art olarak gösterilen size daha önce bahsettiğim [Graphicionado](https://mrmgroup.cs.princeton.edu/papers/taejun_micro16.pdf), traversal irregularity'i çözmek için scratchpad memory kullanıyor ama diğer irregularity'lere bir çözümü yok.

Başka bir [paper](https://seal.ece.ucsb.edu/sites/seal.ece.ucsb.edu/files/publications/hpca-2019-abanti.pdf)'da da yine traversal irregularity'i çözmek için yeni bir prefetcher önerilmiş.

Mustafa Özdal'la beraber yazdığınız [paper](http://repository.bilkent.edu.tr/bitstream/handle/11693/37725/Energy%20Efficient%20Architecture%20for%20Graph%20Analytics%20Accelerators.pdf?sequence=1&isAllowed=y)'da da update irregularity'i çözmek için bit vector kullanmışşsınız (active vertex'leri tutmak için kullandığınız bit vector).

Son olarak da [Graphdyns](https://web.ece.ucsb.edu/~iakgun/files/MICRO2019.pdf) adında bir architecture önerilmiş geçtiğimiz yılın sonlarında. Bu [paper](https://web.ece.ucsb.edu/~iakgun/files/MICRO2019.pdf)'da ise vertex centric programming model'i optimize edip run time'ı edge count'dan haberdar ederek exact edge prefetching'i mümkün kılmış (Traversal irregularity'i böyle çözmüşler). Bu programlama modelinde ayrıca workload size'ı da paylaştıkları için thread'lere paylaştırılan workload'ları da dengelemeyi başarmışlar (workload irregularity'i çözüyor). Update irregularity'i de sizin yazdığın paper'daki gibi bitmap kullanarak çözmüşler. Yani üç soruna da çözüm bulmuşlar.

Graphdyns şu an state of art gibi gözüküyor. Bundan daha farklı ne yapılabilir diye çok düşündüm açıkçası ama pek ilerleme kaydedemedim. O yüzden sizin görüşlerinizi almak istedim.