provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}

resource "aws_security_group" "kube_master" {
  name        = "kube_master"
  description = "Allow kube master inbound traffic"

  ingress {
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
      from_port   = 10250
      to_port     = 10252
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
    
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "_1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "kube_worker" {
  name        = "kube_worker"
  description = "Allow kube worker inbound traffic"

  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
   
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "_1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

  resource "aws_key_pair" "terraform_kube_key" {
	key_name = "terraform_kube_key"
    public_key = "${file("/home/noah/.ssh/terraform_kube_key.pub")}"
  }

resource "aws_instance" "kube_master" {
  ami = "${var.ami}"
  instance_type = "${var.instance}"
  count = "${var.master_count}"
  key_name = "${aws_key_pair.terraform_kube_key.key_name}"
  security_groups = ["${aws_security_group.kube_master.name}"]

  provisioner "remote-exec" {
        inline = [
          "sudo sed _i _r  's/127.0.0.1 localhost/127.0.0.1 localhost kube_master/' /etc/hosts",
          "curl _s _O https://packages.cloud.google.com/apt/doc/apt_key.gpg",
          "sudo apt_key add ./apt_key.gpg",
          "sudo add_apt_repository _y 'deb http://apt.kubernetes.io/ kubernetes_xenial main'",
          "sudo apt_get _y _qq update",
          "sudo apt_get _y _qq upgrade",
          "sudo apt_get install _y _q apt_transport_https docker.io",
          "sudo systemctl start docker.service",
          "sudo apt_get _y _q update",
          "sudo apt_get install _y _q htop kubelet kubeadm kubectl kubernetes_cni",
          "sudo service kubelet restart",
          "sudo kubeadm init __token ${var.kube_token} __kubernetes_version ${var.kube_version}",
          "sudo cp _v /etc/kubernetes/admin.conf /home/ubuntu/config",
          "sudo chown ubuntu /home/ubuntu/config",
          "kubectl apply _f https://git.io/weave_kube",
        ]
	}  
}


resource "aws_instance" "kube_worker" {
  ami   = "${var.ami}"
  instance_type = "${var.instance}"
  count = "${var.worker_count}"
  key_name = "${aws_key_pair.terraform_kube_key.key_name}"
  security_groups = ["${aws_security_group.kube_worker.name}"]
  depends_on      = ["aws_instance.kube_master"]
  
  provisioner "remote-exec" {
      inline = [
        "sudo sed _i _r  's/127.0.0.1 localhost/127.0.0.1 localhost kube_master/' /etc/hosts",
        "curl _s _O https://packages.cloud.google.com/apt/doc/apt_key.gpg",
        "sudo apt_key add apt_key.gpg",
        "sudo add_apt_repository 'deb http://apt.kubernetes.io/ kubernetes_xenial main'",
        "sudo apt_get _y _q update",
        "sudo apt_get _y _q upgrade",
        "sudo apt_get install _y _q apt_transport_https docker.io",
        "sudo systemctl start docker.service",
        "sudo apt_get _y _q update",
        "sudo apt_get install _y _q htop kubelet kubeadm kubectl kubernetes_cni",
        "sudo service kubelet restart",
        "sudo kubeadm join __token ${var.kube_token} ${aws_instance.kube_master.public_ip}",
      ]
	}
}