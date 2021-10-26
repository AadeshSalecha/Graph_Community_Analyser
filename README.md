# Graph_Community_Analyser

This repository was is linked to work that was used in the paper - *Detecting fake news spreaders in social networks using inductive representation learning*. This paper was published in the IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM) 2020.

Please note that the code is still in a maintenance state.

If you find this code or paper useful in your research, please consider citing:

Please cite this paper:

```
@inproceedings{rath2020detecting,
  title={Detecting fake news spreaders in social networks using inductive representation learning},
  author={Rath, Bhavtosh and Salecha, Aadesh and Srivastava, Jaideep},
  booktitle={2020 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM)},
  pages={182--189},
  year={2020},
  organization={IEEE}
}
```

This project contains IGraph and NetworkX implementations of the following repo:
https://github.com/BhavtoshRath/l1_community_ops

It also contains the latest implementations for TSM calculation based on:
https://github.com/BhavtoshRath/TSM_python

The following functionality is not working as of 7.27.19:

a) second_level stats for IGraph implementation

b) spreader_role stats for both NetworkX and IGraph implementaion

c) Igraph implementation for bel_ranks is working (but needs to be validated against ground truth)
