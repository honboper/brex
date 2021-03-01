from urllib import parse

url = 'https://mercedes.catalogs-parts.com/cat_scripts/get_part.php?catalog=eu&lang=en&maybach=0&wheel_class=1&classname=c-klasse&modelname=c+220+cdi&set_aggtyp=fg&catalogcode=61R   &modelcode=204002&set_spmno=0&set_spmaggtyp=FG&set_spmaggmdl=0&set_spmaggcat=0&set_group=42&set_sanum=0&set_subgrp=030&set_stroke=0&set_sasubgrp=0&param=vin:WDDGF0CB5DA744306&client=1&_=1614491468179'

a = parse.quote(url)

print(a)