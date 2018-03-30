# -*- coding: utf-8 -*-

"""
Retrieve historical data from CIMISS service.
"""

import os
import calendar
import numpy as np
from dk_met_io.retrieve_cimiss_server import cimiss_obs_by_time_range
from dk_met_io.retrieve_cimiss_server import cimiss_obs_in_rect_by_time_range


def get_day_hist_obs(years=np.arange(2000, 2011, 1),
                     month_range=(1, 12),
                     elements=None,
                     sta_levels=None,
                     outfname='day_rain_obs',
                     outdir='.'):
    """
    Download historical daily observations and write to data files,
    each month a file.

    :param years: years for historical data
    :param month_range: month range each year, like (1, 12)
    :param elements: elements for retrieve, 'ele1, ele2, ...'
    :param sta_levels: station levels
    :param outfname: output file name + '_year' + '_month'
    :param outdir: output file directory
    :return: output file names.

    :Example:
    >>> get_day_hist_obs(years=np.arange(2000, 2016, 1), outdir="D:/")

    """

    # check elements
    if elements is None:
        elements = "Station_Id_C,Station_Name,Datetime,Lat,Lon,PRE_Time_0808"

    # check output directory
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # define months
    months = np.arange(1, 13, 1)

    # Because of the CIMISS data mount limit,
    # so loop every year to download the data.
    out_files = []
    for iy in years:
        if calendar.isleap(iy):
            last_day = ['31', '29', '31', '30', '31', '30',
                        '31', '31', '30', '31', '30', '31']
        else:
            last_day = ['31', '28', '31', '30', '31', '30',
                        '31', '31', '30', '31', '30', '31']

        for i, im in enumerate(months):
            # check month range
            if not (month_range[0] <= im <= month_range[1]):
                continue

            month = '%02d' % im
            start_time = str(iy) + month + '01' + '000000'
            end_time = str(iy) + month + last_day[i] + '000000'
            time_range = "[" + start_time + "," + end_time + "]"

            # retrieve observations from CIMISS server
            data = cimiss_obs_by_time_range(
                time_range, sta_levels=sta_levels,
                data_code="SURF_CHN_MUL_DAY", elements=elements)
            if data is None:
                continue

            # save observation data to file
            out_files.append(os.path.join(
                outdir, outfname + "_" + str(iy) + "_" + month + ".pkl"))
            data.to_pickle(out_files[-1])

    return out_files


def get_mon_hist_obs(years=np.arange(2000, 2011, 1),
                     limit=(3, 73, 54, 136),
                     elements=None,
                     outfname='mon_surface_obs',
                     outdir='.'):
    """
    Download historical monthly observations and write to data files,
    each year a file.

    :param years: years for historical data
    :param limit: spatial limit [min_lat, min_lon, max_lat, max_lon]
    :param elements: elements for retrieve, 'ele1, ele2, ...'
    :param outfname: output file name + 'year'
    :param outdir: output file directory
    :return: Output filenames
    """

    # check elements
    if elements is None:
        elements = ("Station_Id_C,Station_Name,Year,"
                    "Mon,Lat,Lon,Alti,PRE_Time_0808")

    # check output directory
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Loop every year to download the data.
    out_files = []
    for iy in years:
        # check out file
        outfile = os.path.join(outdir, outfname + "_" + str(iy) + ".pkl")
        if os.path.isfile(outfile):
            continue

        # set time range
        start_time = str(iy) + '0101' + '000000'
        end_time = str(iy) + '1201' + '000000'
        time_range = "[" + start_time + "," + end_time + "]"

        # retrieve observations from CIMISS server
        data = cimiss_obs_in_rect_by_time_range(
            time_range, limit, data_code='SURF_CHN_MUL_MON',
            elements=elements)
        if data is None:
            continue

        # save observation data to file
        out_files.append(outfile)
        data.to_pickle(out_files[-1])

    return out_files
