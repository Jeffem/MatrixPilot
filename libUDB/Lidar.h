/* 
 * File:   Lidar.h
 * Author: gfm
 *
 * Created on 26 janvier 2016, 16:24
 */
// This file is part of MatrixPilot.
//
//    http://code.google.com/p/gentlenav/
//
// Copyright 2009-2011 MatrixPilot Team
// See the AUTHORS.TXT file for a list of authors of MatrixPilot.
//
// MatrixPilot is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// MatrixPilot is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with MatrixPilot.  If not, see <http://www.gnu.org/licenses/>.



#ifndef LIDAR_H
#define	LIDAR_H

#define LIDAR_ADDRESS 0xC4  // I2C address of Lidar Lite
#if (USE_LIDAR_ALTITUDE	== 1)
extern int32_t lidar0;// LidarLite value for a null altitude in half millimeters

    typedef void (*lidar_callback_funcptr)(long altitude);
    void rxLidar_on_PWM(lidar_callback_funcptr callback);  // service the Lidar altimeter on PWM

#endif
    
#endif	/* LIDAR_H */

