from cmd import execcmd


uuids = {'98937135-5453-9e00-0298-00d0c7740268': 'drive 1',
         '1bccc6bb-48c9-b000-a613-8db11d2c76f4': 'drive 2'}


class monitor:

    def __init__(self):
        self._static_uuids = uuids

        self._drive_locations = None
        self._drive_info = {}

    @property
    def drive_locations(self):
        if self._drive_locations is not None:
            return self._drive_locations

        search, err = execcmd('blkid')

        temp = {}
        for line in search.split('\n'):
            for uuid in self._static_uuids.keys():
                if uuid in line:
                    temp[self._static_uuids[uuid]] = \
                        line.split(': UUID')[0][:-1]

        return temp

    def poll_drives(self):
        for drive, loc in self.drive_locations.items():
            cmd = f'sudo smartctl -a {loc}'
            # print(f'issuing cmd {cmd}')

            stdout, stderr = execcmd(cmd)

            self._drive_info[drive] = stdout

    @property
    def drive_temps(self):
        self.poll_drives()

        temps = []
        for drive, data in self._drive_info.items():
            for line in data.split('\n'):
                if line.startswith('194'):
                    data = [sec for sec in line.split('  ') if sec != '']
                    t = data[-1].split('(')[0].strip()
                    temps.append(int(t))
                    continue

        return temps

    @property
    def cpu_temp(self) -> float:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as o:
            temp = int(o.read().strip())/1000

        return temp

    @property
    def maxtemp(self):
        return max([self.cpu_temp] + self.drive_temps)


if __name__ == '__main__':
    temp = monitor()

    print(temp.drive_locations)
    print(f'drive temps are: {temp.drive_temps}')

    print(f'CPU temp is {temp.cpu_temp}°C')
    print(f'maxtemp is {temp.maxtemp}')
