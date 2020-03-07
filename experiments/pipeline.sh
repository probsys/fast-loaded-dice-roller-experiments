#!/bin/bash

set -e

if [ -z ${JOBS} ]; then
  NCPU=$(python -c 'import multiprocessing; print(multiprocessing.cpu_count())')
else
  NCPU=${JOBS}
fi

set -u

stamp=${1}
cmd=${2}

SAMPLERS='interval
  alias.exact
  ky.enc
  rej.binary
  rej.enc
  rej.matc
  rej.table
  rej.uniform'

if [ ${cmd} = 'initialize' ]; then
  N=$(echo ${stamp} | cut -d. -f2)
  Z=$(echo ${stamp} | cut -d. -f3)
  seed=$(echo ${stamp} | cut -d. -f4)
  qs=$(echo ${SAMPLERS} | xargs -I% echo "'%'")
  ./dists.py generate-distributions N=${N} Z=${Z} seed=${seed} samplers="${qs}" thin=5;
  exit 0;
fi

if [ ${cmd} = 'aggregate-sizes' ]; then
  for sampler in ${SAMPLERS}; do
      fn=${stamp}/${sampler}.sizes;
      stat ${stamp}/*.${sampler} -c %s > ${fn};
      echo ${fn};
  done
  exit 0;
fi

if [ ${cmd} = 'measure-runtimes' ]; then
  steps=${3}
  seed=$(echo ${stamp} | cut -d. -f4)
  for sampler in ${SAMPLERS}; do
      rm -rf /tmp/w
      fnames=$(ls ${stamp}/*.${sampler});
      for f in ${fnames}; do
          u=${f}.runtime
          echo "./main.out.opt ${seed} ${steps} ${sampler} ${f} > ${u} && echo ${u}" >>/tmp/w
      done
      echo measuring ${sampler}
      cat /tmp/w | xargs -P ${NCPU} -n1 -d'\n' -I% sh -c '%'
      wait
  done
  exit 0;
fi

if [ ${cmd} = 'aggregate-runtimes' ]; then
  for sampler in ${SAMPLERS}; do
      fn_runtime=${stamp}/${sampler}.runtimes;
      fn_calls=${stamp}/${sampler}.calls;
      fnames=$(ls ${stamp}/*.${sampler}.runtime)
      rm -rf ${fn_runtime} ${fn_calls};
      for f in ${fnames}; do
          echo $f
          cat ${f} | tail -n1 | cut -f2 -d ' ' >> ${fn_runtime}
          cat ${f} | tail -n1 | cut -f3 -d ' ' >> ${fn_calls}
      done
      echo ${fn_runtime};
      echo ${fn_calls};
  done
  exit 0;
fi

if [ ${cmd} = 'run-all-memory-runtime' ]; then
  Z=${3}
  for n in ${4}; do
      stamp=dists.${n}.${Z}.2
      echo ${stamp}
      ./pipeline.sh ${stamp} initialize;
      ./pipeline.sh ${stamp} aggregate-sizes;
      ./pipeline.sh ${stamp} measure-runtimes 1000000;
      ./pipeline.sh ${stamp} aggregate-runtimes;
  done
  exit 0
fi

# The Ns are designed to be linearly spaced on log scale.
Ns_pp='2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 19 21 23 25 27 29 31 34 36 39 42 46 50 54 58 63 68 73 79 85 92 100 107 116 125 135 146 158 171 184 199 215 232 251 271 292 316 341 368 398 429 464 501 541 584 630 681 735 794 857 926 1000 1079 1165 1258 1359 1467 1584 1711 1847 1995 2154 2326 2511 2712 2928 3162 3414 3686 3981 4298 4641 5011 5411 5843 6309 6812 7356 7943 8576 9261 10000 12589 15848 19952 25118 31622 39810 50118 63095 79432'
Zs_pp='10 100 1000 10000 100000 1000000'
# Ns_pp='10 20 30'
# Zs_pp='10 15 50'
if [ ${cmd} = 'preprocess-initialize' ]; then
  seed=$(echo ${stamp} | cut -d. -f3);
  mkdir -p ${stamp};
  counter=0
  for n in ${Ns_pp}; do (
    for Z in ${Zs_pp}; do
      if [ ${n} -lt ${Z} ]; then
        d=dists.${n}.${Z}.${seed}
        ./dists.py generate-distributions \
            N=${n} Z=${Z} seed=${seed} samplers='none'\
            thin=600 offset=500;
        for x in $(ls ${d}/*); do
          fx=$(echo $x | tr '/' '.' | sed 's/d.00000.//g')
          dx=${stamp}/${fx};
          mv $x ${dx};
          echo ${dx};
        done
        rm -rf ${d};
      fi
    done
    wait;
  ) &
  counter=$((counter + 1))
  if [ ${counter} -eq 60 ]; then
    wait
    counter=0;
  fi
  done
  exit 0
fi

if [ ${cmd} = 'preprocess-measure' ]; then
  fnames=$(ls ${stamp}/*.dist);
  rm -rf /tmp/w
  rm -rf ${stamp}/preprocess
  for fn in ${fnames}; do
      u=${fn%.dist}.preprocess
      echo "./preprocess.out.opt ${fn} > ${u}.c && echo ${u}.c" >> /tmp/w
  done
  cat /tmp/w | xargs -P ${NCPU} -n1 -d'\n' -I% sh -c '%'
  cat ${stamp}/*.preprocess.c > ${stamp}/preprocess
  echo ${stamp}/preprocess
  exit 0;
fi

if [ ${cmd} = 'preprocess-aggregate' ]; then
  seed=$(echo ${stamp} | cut -d. -f3);
  Zs=$(ls ${stamp}/dists.*.c | cut -f2 -d/ | cut -f3 -d. | sort | uniq);
  Ns=$(ls ${stamp}/dists.*.c | cut -f2 -d/ | cut -f2 -d. | sort -h | uniq);
  for Z in ${Zs}; do
    fout=${stamp}/aggregate.${Z}.preprocess
    rm -rf ${fout}.c;
    rm -rf ${fout}.cpp;
    for n in ${Ns}; do
      if [ ${n} -lt ${Z} ]; then
        cat ${stamp}/dists.${n}.${Z}.${seed}.preprocess.c >> ${fout}.c;
      fi
    done
    echo ${fout}.c
  done
  exit 0
fi

echo 'Unknown command' ${cmd};
exit 1
