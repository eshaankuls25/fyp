from pcapy import findalldevs, open_live
from impacket import ImpactDecoder, ImpactPacket
from impacket.ImpactPacket import IP, TCP, UDP, ICMP
from extractdata import ExtractData
import sys

def getInterface():

	#Get list of all network interfaces available for listening on
	interfaces = findalldevs()

	if len(interfaces) < 1:
		print "\nThere are no network interfaces available, "
		+"or you do not have the correct permissions to view them.\n"

	#If a single interface has been found...
	if len(interfaces) == 1:
		interface = interfaces[0]
	else:
		print "Network interfaces:\n"
		for i in range(len(interfaces)):
			print "---%i - %s\n" %(i+1, interfaces[i])
		
		while True:
			input = raw_input("Select an interface to scan, or press 0 to quit: ")
			try:
				i = int(input)
				if i == 0:
					interface = None
					break
				interface = interfaces[i-1]	
				break
			except(SyntaxError, ValueError):
				pass
	return interface

def listenForPackets(interface):

	#Start live capture
	reader = open_live(interface, 1500, 0, 100) #2nd param - bytes to capture - 1500 bytes for Ethernet MTU - Max TCP size is 65536. 
												#Same as UDP, but UDP usually sent in chunks of 512 bytes
												#3rd - put interface in promiscuous mose
												#4th - timeout in milliseconds
	#Set TCP only filter
	reader.setfilter("ip proto \\tcp")

	#Run packet capture
	reader.loop(0, callback)

def callback (header, data):
	src_ip = None; dst_ip = None
	src_port = None; dst_port = None
	layer4Type = ""
	output = ""
	payloadSize = 0;
	extract = ExtractData()

	#Parse packet
	decoder = ImpactDecoder.EthDecoder()
	packet = decoder.decode(data)

	#Parse IP packet inside ethernet one
	iphdr = packet.child()

	if isinstance(iphdr, IP):
		#Parse TCP packet inside IP one
		hdr = iphdr.child()

		if isinstance(hdr, TCP) or isinstance(hdr, UDP):
			if isinstance(hdr, TCP):
				layer4Type = "TCP"
				#Only look at SYN packets, not ACK ones
				if hdr.get_SYN() and not hdr.get_ACK():
					#Get src and dest IPs
					src_ip = iphdr.get_ip_src()
					dst_ip = iphdr.get_ip_dst()
					src_port = hdr.get_th_dport()
					dst_port = hdr.get_th_sport()
					payloadSize = hdr.get_size()-hdr.get_header_size()
			elif isinstance(hdr, UDP):
				layer4Type = "UDP"
				#Get src and dest IPs
				src_ip = iphdr.get_ip_src()
				dst_ip = iphdr.get_ip_dst()
				src_port = hdr.get_th_dport()
				dst_port = hdr.get_th_sport()
				payloadSize = hdr.get_size()-hdr.get_header_size()

			#Results are printed
			output = "(%s) Connection attempted from: %s:%s to: %s:%s\n" %(layer4Type, src_ip, src_port, dst_ip, dst_port)
			if(payloadSize != 0):
				output += "\nPayload size: %d\n----%s----\n----\n" %(payloadSize, hdr.get_data_as_string())
			print output
		
		if(src_ip and dst_ip):
			extract.writeToFile("packetOutput.txt", output, "a")
	else:
		print "\nIP header doesn't exist.\n";
		iphdr = None		

def runProcess():
        print "\nEnter a program to run, with some arguments, if required.\n"
        cmdLine = raw_input()
        argsList = shlex.split(self.cmdLine)
        ioInstance = InputOutput(argsList)

def main():
	interface = getInterface()
	if interface:
		listenForPackets(interface)

if __name__ == "__main__":
	main()








