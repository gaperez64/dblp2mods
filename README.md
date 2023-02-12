# dblp2mods
A script to translate DBLP xml into (FWO-friendly) MODS xml

## Notes
* The script will ignore all publications that are not of (FWO) type A1 and
  C1.
* It will also ignore all informal publications (e.g. those submitted to
  arxiv).
* To get the FWO parser to believe the journal articles are indeed A1, an
  empty (World-of-Science) impact factor is entered.
