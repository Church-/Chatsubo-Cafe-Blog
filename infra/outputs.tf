output "master_public_ip" {
  value = "${aws_instance.kube_master.*.public_ip}"
}
output "worker_public_ip" {
  value = "${aws_instance.kube_worker.*.public_ip}"
}