resource "proxmox_vm_qemu" "your-vm" {
  count       = 1
  target_node = "pve"
  vmid        = "152"
  name        = "qemu-vm${count.index + 10}"
  desc        = "Cloud-init VM from template"
  onboot      = true

  # Clone from template
  clone      = "terraria"
  full_clone = true
  os_type    = "cloud-init"

  # VM System Settings
  agent   = 1
  cores   = 4
  sockets = 1
  cpu     = "host"
  memory  = 4096

  # Add a disk (scsi0)
  disk {
    size     = "20G"       # Disk size
    type     = "disk"      # Disk type (this is the correct type)
    storage  = "local-lvm" # Your Proxmox storage pool
    slot     = "scsi0"     # Specify the slot for the disk (valid slot like 'scsi0')
    iothread = true        # Enable I/O thread for better performance
  }

  # Add cloud-init drive (ide2)
  disk {
    type    = "cloudinit"
    storage = "local-lvm" # Storage location for cloud-init disk
    slot    = "ide2"      # Set the slot to ide2 for cloud-init
  }

  # Ensure the boot order is correct
  bootdisk = "scsi0"
  boot     = "order=scsi0;net0;ide2"
  tablet   = false

  # Networking
  network {
    bridge = "vmbr0"
    model  = "virtio"
  }

  # Cloud-Init IP configuration
  ipconfig0 = "ip=192.168.1.11${count.index + 1}/24,gw=192.168.1.1"

  # Cloud-Init user configuration
  ciuser  = "neko"
  sshkeys = <<EOF
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtLlotoF3lYnM0mkbAjpaEMOJXLllpu97oN93w8VEJO6q+S/9pXPa+2he36RkJ9BOnSq1HCSzj61u3j9dV4K9FTOyodNfOsEcbN7jNjH5I+UC8ZbsZb6nf0wksXK+4iR7nBBzQdEmsmz9dbwR5fwrHN66WniE63N0fm3bozrQzIAzqbjLpdQd7Cpz9sLzAMFCGb6G5gQdcMHQ7SNDBSktiQ7KOnzOLBLbni7MuthQBNjCd3jIF4WEBIGeyq2tBKOnXzIixjs012gamCN5YB3ErXIx8mMjmv7Z1J73LwhRNSwug4heGyXN6YPMN7mWMWDkiwbzBq0X6qciFt3kT2tar m1
  EOF

  # Add connection block to allow remote-exec provisioner to work
  provisioner "remote-exec" {
    inline = [
      "hostname",
    ]

    connection {
      type        = "ssh"
      user        = "neko"                           # The cloud-init user specified above
      private_key = file("~/.ssh/id_rsa")            # Path to your private SSH key
      host        = "192.168.1.11${count.index + 1}" # The IP assigned via cloud-init
    }
  }
}
